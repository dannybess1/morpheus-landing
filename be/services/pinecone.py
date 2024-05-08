
from database import pc
from .singleton import singleton
import logging
import struct

@singleton
class PineconeService:

    def __init__(self):
        self.namespace = "proteus-testing"
        self.index = pc.Index("proteus-testing")

        self.neural_namespace = "proteus-testing-neural"
        self.neural_index = pc.Index("proteus-testing-neural")

        self.color_namespace = "proteus-testing-color"
        self.color_index = pc.Index("proteus-testing-color")

        self.block_namespace = "proteus-testing-block"
        self.block_index = pc.Index("proteus-testing-block")

    # TODO: for each of our perceptual hashes we want to insert them based on the images id in the sql db
    def insert(self, id, hashes):
        ## Slice up the hashes into 8 limbs 
        ## Insert the 8 limbs into the index

        def convert_to_float_array(value):
            return [float(int(value[i:i+8], base=16)) for i in range(0, len(value), 8)]
            
        # blockhash
        blockhash_values = convert_to_float_array(hashes["blockhash"])
        self.block_index.upsert(vectors=[{"id": id, "values": blockhash_values}], namespace=self.block_namespace)

        # neuralhash
        neuralhash_values = convert_to_float_array(hashes["neuralhash"])
        self.neural_index.upsert(vectors=[{"id": id, "values": neuralhash_values}], namespace=self.neural_namespace)

        # colorhash
        colorhash_values = convert_to_float_array(hashes["colourhash"])
        self.color_index.upsert(vectors=[{"id": id, "values": colorhash_values}], namespace=self.color_namespace)

        logging.info(f"Inserted hashes into Pinecone")

        
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