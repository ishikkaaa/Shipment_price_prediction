import sys
import os
from shipment.logger import logging
from pandas import DataFrame
from sklearn.model_selection import train_test_split
from typing import Tuple
from shipment.exceptions import shippingException
from shipment.configurations.mongo_operations import MongoDBOperation
from shipment.entity.config_entity import DataIngestionConfig
from shipment.entity.artifacts_entity import DataIngestionArtifacts
from shipment.constants import TEST_SIZE

class Data_Ingestion:
  def __init__(self,data_ingestion_config:DataIngestionConfig,mongo_op:MongoDBOperation):
    self.data_ingestion_config=data_ingestion_config
    self.mongo_op=mongo_op

  def get_data_from_mongodb(self)->DataFrame:
    logging.info("Entered get_data_from_mongodb method of Data_ingestion class")
    try:
      logging.info("Getting the dataframe from mongodb")
      df=self.mongo_op.get_collection_as_dataframe(self.data_ingestion_config.DB_NAME,self.data_ingestion_config.COLLECTION_NAME)
      logging.info('Got the dataframe from mongodb')
      logging.info('Exited the get_data_from_mongodb of Data_Ingestion class')
      return df
    except Exception as e:
      raise shippingException(e,sys) from e

  #this method will split the data
  def split_data_as_train_test(self,df)->Tuple[DataFrame,DataFrame]:
    logging.info('Entered split_data_as_train_test method of Dat_ingestion class')
    try:
      os.mkdirs(self.data_ingestion_config.DATA_INGESTION_ARTIFCATS_DIR,exist_ok=True)
      train_set,test_set=train_test_split(df,test_size=TEST_SIZE)
      logging.info('Performed a train-test split on dataset')
      os.makedirs(self.data_ingestion_config.TRAIN_DATA_ARTIFACT_FILE_DIR,exist_ok=True)
      logging.info(f"created {os.path.basename(self.data_ingestion_config.TRAIN_DATA_ARTIFACT_FILE_DIR)} directory")
      os.makedirs(self.data_ingestion_config.TEST_DATA_ARTIFACT_FILE_DIR,exist_ok=True)
      logging.info(f"created {os.path.basename(self.data_ingestion_config.TEST_DATA_ARTIFACT_FILE_DIR)} diretory")
      train_set.to_csv(
        self.data_ingestion_config.TRAIN_DATA_FILE_PATH,
        index=False,
        header=True
      )
      test_set.to_csv(
        self.data_ingestion_config.TEST_DATA_FILE_PATH,
        index=False,
        header=True
      )
      logging.info('Converted train and test df to csv')
      logging.info(f"Saved {os.path.basename(self.data_ingestion_config.TRAIN_DATA_FILE_PATH)}, \{os.path.basename(self.data_ingestion_config.TEST_DATA_FILE_PATH)} in \ {os.path.basename(self.data_ingestion_config.DATA_INGESTION_ARTIFCATS_DIR)}.")
      logging.info('Exited split_data_as_train_test of Data_Ingestion class')
      return train_set,test_set
    except Exception as e:
      raise shippingException(e,sys) from e
    

  #this method initiate the data ingestion
  def initiate_data_ingestion(self)->DataIngestionArtifacts:
    logging.info('Entered initiate_data_ingestion method of Dat_Ingestion class')
    try:
      self.get_data_from_mongodb()
      df1=df.drop(self.data_ingestion_config.DROP_COLS,axis=1)
      df1=df1.dropna()
      logging.info("Got the data from mongodb")

      self.split_data_as_train_test(df1)
      logging.info('Exited from initiate_data_ingestion method of Data_ingestion class')
      data_ingestion_artifacts=DataIngestionArtifacts(self.data_ingestion_config.TRAIN_DATA_FILE_PATH,self.data_ingestion_config.TEST_DATA_FILE_PATH)
      return data_ingestion_artifacts
    except Exception as e:
      raise shippingException(e,sys) from e

