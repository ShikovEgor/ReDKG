import random

import numpy as np
import torch
import torch.optim as optim
from env import Simulator
from redkg.models.gcn_gru_layers import Net
from torch import Tensor


def train_kge_model(kge_model, train_pars, info, train_triples, valid_triples, max_steps=10):
    print("Training...")
    optimizer = torch.optim.Adam(filter(lambda p: p.requires_grad, kge_model.parameters()), lr=train_pars.learning_rate)

    train_dataloader_head = DataLoader(
        TrainDataset(
            train_triples,
            info["nentity"],
            info["nrelation"],
            train_pars.negative_sample_size,
            "head-batch",
            info["count"],
            info["true_head"],
            info["true_tail"],
            info["entity_dict"],
            negative_mode="full",
        ),
        batch_size=train_pars.train_batch_size,
        shuffle=True,
        num_workers=max(1, train_pars.cpu_num // 2),
        collate_fn=TrainDataset.collate_fn,
    )

    train_dataloader_tail = DataLoader(
        TrainDataset(
            train_triples,
            info["nentity"],
            info["nrelation"],
            train_pars.negative_sample_size,
            "tail-batch",
            info["count"],
            info["true_head"],
            info["true_tail"],
            info["entity_dict"],
            negative_mode="full",
        ),
        batch_size=train_pars.train_batch_size,
        shuffle=True,
        num_workers=max(1, train_pars.cpu_num // 2),
        collate_fn=TrainDataset.collate_fn,
    )
    train_iterator = BidirectionalOneShotIterator(train_dataloader_head, train_dataloader_tail)

    training_logs = []
    test_logs = []

    # Training Loop
    for step in range(max_steps):
        log = kge_model.train_step(kge_model, optimizer, train_iterator, train_pars)
        training_logs.append(log)

        if train_pars.do_test:
            metrics = kge_model.test_step(kge_model, valid_triples, train_pars, info["entity_dict"])
            test_logs.append(metrics)

        return training_logs, test_logs


def train(config, item_vocab, model, optimizer):
    memory = deque(maxlen=10000)
    policy_net = Net()
    target_net = Net()
    TARGET_UPDATE = 100
    BATCH_SIZE = 10

    def tmp_Q_eps_greedy(state, actions):
        epsilon = 0.3
        state = torch.tensor(state, dtype=torch.float)
        out = policy_net.forward(state)
        out = out.detach().numpy()
        coin = random.random()
        if coin < epsilon:
            return actions[np.random.choice(range(len(actions)))]
        else:
            return actions[np.argmax(out)]

    def memory_sampling(memory: Tensor):
        mini_batch = random.sample(memory, BATCH_SIZE)
        s_lst, a_lst, r_lst, s_prime_lst, done_mask_lst = [], [], [], [], []

        for transition in mini_batch:
            t_state, t_action, t_reward, t_next_state, t_done = transition
            s_lst.append(t_state)
            a_lst.append([t_action])
            r_lst.append([t_reward])
            s_prime_lst.append(t_next_state)
            done_mask_lst.append([t_done])
        return (
            torch.tensor(s_lst, dtype=torch.float),
            torch.tensor(a_lst),
            torch.tensor(r_lst),
            torch.tensor(s_prime_lst, dtype=torch.float),
            torch.tensor(done_mask_lst),
        )

    def optimize_model(memory: Tensor):
        state_batch, action_batch, reward_batch, next_state_batch, done_batch = memory_sampling(memory)
        state_action_values = policy_net(state_batch)
        next_state_values = target_net(next_state_batch)
        for next_state_value in next_state_values:
            max_val = max(next_state_value).tolist()
            max_val_list.append(max_val)
        expected_state_action_values = state_action_values.tolist()
        for i in range(len(state_action_values)):
            action = action_batch[i]
            expected_state_action_values[i][action] = (max_val_list[i] * GAMMA) + reward_batch[i]
        expected_state_action_values = torch.tensor(expected_state_action_values)
        loss = F.smooth_l1_loss(state_action_values, expected_state_action_values)
        # print('loss', loss)
        optimizer = optim.RMSprop(self.policy_net.parameters())
        optimizer.zero_grad()
        loss.backward()
        for param in self.policy_net.parameters():
            param.grad.data.clamp_(-1, 1)
        optimizer.step()

    simulator = Simulator(config=config, mode="train")
    num_users = len(simulator)
    total_step_count = 0
    for e in range(config.epochs):
        for u in range(num_users):
            user_id, item_ids, rates = simulator.get_user_data(u)
            candidates = []
            done = False
            print("user_id:", user_id)
            for t, (item_id, rate) in enumerate(zip(item_ids, rates)):
                if t == len(item_ids) - 1:
                    done = True
                print("t", t, "item_id", item_id, "rate", rate)
                # TODO
                # Embed item using GCN Algorithm1 line 6 ~ 7
                item_idx = item_id
                embedded_item_state = model.forward_gcn(item_idx)  # (50)
                embedded_user_state = model(item_idx)  # (20)

                # TODO
                # Candidate selection and embedding
                if rate > config.threshold:
                    n_hop_dict = model.get_n_hop(item_id)
                    candidates.extend(n_hop_dict[1])
                    candidates = list(set(candidates))  # Need to get rid of recommended items

                candidates_embeddings = model.forward_gcn(torch.tensor(candidates))
                print("candidate shape:", candidates_embeddings.shape)
                # candidates_embeddings = item_ids  # Embed each item in n_hop_dict using each item's n_hop_dict
                # candidates_embeddings' shape = (# of candidates, config.item_embed_dim)

                # Recommendation using epsilon greedy policy
                recommend_item_id = tmp_Q_eps_greedy(state=embedded_user_state, actions=candidates_embeddings)
                reward = simulator.step(user_id, recommend_item_id)

                # TODO
                # Q learning
                # Store transition to buffer
                state, action, reward, next_state, done = (
                    embedded_state,
                    recommend_item_id,
                    reward,
                    tmp_state_embed(x.append(recommend_item_id)),
                    done,
                )
                Tuple = (state, action, reward, next_state, done)
                memory.append(Tuple)
                # target update
                total_step_count += 1
                if total_step_count % TARGET_UPDATE == 0:
                    target_net.load_state_dict(policy_net.state_dict())
                if len(memory) > 100:
                    optimize_model(memory)
