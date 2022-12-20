class Config:
    """Basic config instance for ReDKG"""

    def __init__(self):
        self.dataset_name = "movie"
        self.raw_data_dir = "./raw_data"
        self.preprocess_results_dir = f"./data/{self.dataset_name}"

        # Raw data file paths
        self.kg_path = f"{self.raw_data_dir}/{self.dataset_name}/kg.txt"
        self.item2entity_path = f"{self.raw_data_dir}/{self.dataset_name}/item_index2entity_id.txt"
        self.rating_path = f"{self.raw_data_dir}/{self.dataset_name}/ratings.csv"
        self.attribute_path = f"{self.raw_data_dir}/{self.dataset_name}/attributes.csv"

        # Parameters to preprocess ratings.csv
        self.separator = ","
        self.threshold = 3  # Threshold of rating to distinguish pos and neg reaction
        self.minimum_interactions = 200  # Remove user with less than 200 interactions

        # Parameters to preprocess kg.txt
        self.hops = 2

        # Parameters to split train test val
        self.train_proportion = 0.8
        self.test_proportion = 0.1
        self.validation_proportion = 0.1
        assert sum([self.train_proportion, self.test_proportion, self.validation_proportion]) == 1.0

        # KGQR train
        self.epochs = 100
        self.item_embed_dim = 50  # Dimension of item embedding
        self.state_embed_dim = 20  # Dimension of user embedding

        