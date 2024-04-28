
from database import pc
from singleton import singleton

@singleton
class PineconeService:

    def __init__(self):
        self.namespace = "proteus-testing"
        self.index = pc.Index("proteus-testing")

    # TODO: for each of our perceptual hashes we want to insert them based on the images id in the sql db
    def insert(self, id, hashes):
        ## Slice up the hashes into 8 limbs 
        ## Insert the 8 limbs into the index
        vectors = []
        models = ["neural_hash", "block_hash", "color_hash"] # TODO: check ordering
        for i, hash in enumerate(hashes):
            values = [hash[i:i+8] for i in range(0, len(hash), 8)]
            id = f"{id}-{models[i]}"
            metadata = {"hash": hash, "model": models[i]} 

            vec = {
                "id": id,
                "values": values,
                "metadata": metadata
            }
            vectors.push(vec)

        # TODO: check correct namespace
        self.index.upsert(vectors=vectors, namespace=self.namespace)

        
    def search(self, hash):
        ## Slice up the hash into 8 limbs
        ## Search the index for the 8 limbs
        ## Return the results
        values = [hash[i:i+8] for i in range(0, len(hash), 8)]

        results = self.index.query(
            namespace=self.namespace,
            vector=values,
            top_k=10,
            include_values=True,
            include_metadata=True
        ) 
        return results