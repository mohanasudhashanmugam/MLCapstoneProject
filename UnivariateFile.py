import pandas as pd
import numpy as np

class UnivariateClass:

    def QuanQual(dataset):
        Quan=[]
        Qual=[]
        for colname in dataset.columns:
            if dataset[colname].dtype == 'O' :
                Qual.append(colname)
            else:
                Quan.append(colname)        
        return Quan,Qual

    def univariate_descriptive(dataset,Quan):
        descriptive=pd.DataFrame(index=["Mean","Median","Mode","Q1-25%","Q2-50%","Q3-75%","99%","Q4-100%","IQR","1.5rule","Lesser_range","Greater_range","Min","Max","kurtosis","skew","variance","std"],columns=Quan)
        
        for columnname in Quan:
            descriptive[columnname]["Mean"]=dataset[columnname].mean()
            descriptive[columnname]["Median"]=dataset[columnname].median()
            descriptive[columnname]["Mode"]=dataset[columnname].mode()[0]
            descriptive[columnname]["Q1-25%"]=dataset.describe()[columnname]["25%"]
            descriptive[columnname]["Q2-50%"]=dataset.describe()[columnname]["50%"]
            descriptive[columnname]["Q3-75%"]=dataset.describe()[columnname]["75%"]
            descriptive[columnname]["99%"]=np.nanpercentile(dataset[columnname], 99)
            descriptive[columnname]["Q4-100%"]=dataset.describe()[columnname]["max"]
            descriptive[columnname]["IQR"]=descriptive[columnname]["Q3-75%"]-descriptive[columnname]["Q1-25%"]
            descriptive[columnname]["1.5rule"]=1.5*descriptive[columnname]["IQR"]
            descriptive[columnname]["Lesser_range"]=descriptive[columnname]["Q1-25%"]-descriptive[columnname]["1.5rule"]
            descriptive[columnname]["Greater_range"]=descriptive[columnname]["Q3-75%"]+descriptive[columnname]["1.5rule"]
            descriptive[columnname]["Min"]=dataset[columnname].min()
            descriptive[columnname]["Max"]=dataset[columnname].max()
            descriptive[columnname]["kurtosis"]=dataset[columnname].kurtosis()
            descriptive[columnname]["skew"]=dataset[columnname].skew()
            descriptive[columnname]["variance"]=dataset[columnname].var()
            descriptive[columnname]["std"]=dataset[columnname].std()
        return descriptive 
    
    
    def Identify_Outliers(descriptive,Quan):
        lesser_outlier=[]
        greater_outlier=[]

        for columnname in Quan:
            if descriptive[columnname]["Min"]<descriptive[columnname]["Lesser_range"]:
                lesser_outlier.append(columnname)

            if descriptive[columnname]["Max"]>descriptive[columnname]["Greater_range"]:
                greater_outlier.append(columnname)
        return lesser_outlier,greater_outlier
    
    
    def replace_outliers(dataset,descriptive,lesser_outlier,greater_outlier):

        for columnname in lesser_outlier:
            dataset[columnname][dataset[columnname]<descriptive[columnname]["Lesser_range"]]=descriptive[columnname]["Lesser_range"]
        for columnname in greater_outlier:
            dataset[columnname][dataset[columnname]>descriptive[columnname]["Greater_range"]]=descriptive[columnname]["Greater_range"]

    
    def freqtable(dataset,columnname):
        freqtable=pd.DataFrame(columns=["Uniq_values","Frequency","Rel_Frequency","Cum_Frequency"])
        freqtable["Uniq_values"]=dataset[columnname].value_counts().index
        freqtable["Frequency"]=dataset[columnname].value_counts().values
        freqtable["Rel_Frequency"]=freqtable["Frequency"]/dataset[columnname].value_counts().count()
        freqtable["Cum_Frequency"]=freqtable["Rel_Frequency"].cumsum()
        return freqtable