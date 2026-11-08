import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from wordcloud import WordCloud, STOPWORDS
from sklearn.cluster import KMeans,DBSCAN
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer
from sklearn.decomposition import PCA
import gensim
from nltk.tokenize import sent_tokenize, word_tokenize
import nltk
import re
import numpy as np
nltk.download('punkt')
st.set_option('deprecation.showPyplotGlobalUse', False)

@st.cache_data
def load_data(uploaded_file):
    #df = data.cars()
    df = pd.read_csv(uploaded_file, decimal =',')
    return df


# Create and generate a word cloud image:
@st.cache_data
def create_wordcloud(df,validation, num_clusters=4,model='kmeans',ext_features='word2vec',value_eps=0.1,min_samples=5,metric_distance='cosine'):
    
    df.dropna(subset=['summary'], axis=0, inplace = True)
    summary = df['summary']
    st.text("Histórico de mensagem")
    summary
    all_summary = " ".join(s for s in summary)
    data = []
    stopwords = set(STOPWORDS)
    stopwords.update(["da", "meu", "em", "você", "de", "ao", "os","nosso","nossa","sua",
                      "ele","ela","também","até","un","essa","esse","que"
                      "and","the","a","in","to","with","de","e","for",""])
    pca = PCA(n_components=100)
    # iterate through each sentence in the file
    for review in summary.to_list():
        data_temp = []
        for i in sent_tokenize(review):
            temp = []

            # tokenize the sentence into words
            for j in word_tokenize(i):
                j = re.sub(u'[^a-zA-ZáéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇ:]', '',j)
                if not j.lower() in stopwords:
                        temp.append(j.lower())

            #data.append(np.array(temp).flatten())
            data_temp.append(' '.join(temp))
            
        data.append(' '.join(data_temp))
        
    if ext_features=='word2vec':
        # Create CBOW model
        model1 = gensim.models.Word2Vec([word.split(' ') for word in data], min_count=20,
                                        vector_size=100, window=5,sg=2)
        words = list(w for w in model1.wv.index_to_key)    
        # Make a dictionary
        we_dict = {word:model1.wv[word] for word in words}
        df_vectors=pd.DataFrame(we_dict).transpose()

    elif ext_features=='tf_idf':
        tfidf_vectorizer=TfidfVectorizer(min_df=10)
        text_idf=tfidf_vectorizer.fit_transform(data)

        df_vectors=pd.DataFrame(
            pca.fit_transform( np.asarray(text_idf.todense()).transpose()),
            index=tfidf_vectorizer.get_feature_names_out()
        )
    
    elif ext_features=='count':
        count_vectorizer=CountVectorizer(min_df=10)
        text_count=count_vectorizer.fit_transform(data)

        df_vectors=pd.DataFrame(
            pca.fit_transform( np.asarray(text_count.todense()).transpose()),
            index=count_vectorizer.get_feature_names_out()
        )

    #st.write(df_vectors)
    
    if validation:
        st.subheader("Curva SSE X Clusters")
        st.text("Análise do número ótimo de Clusters")
        sse = {}
        for k in range(1, 15):
            kmeans = KMeans(n_clusters=k, max_iter=1000).fit(df_vectors.values)
            df_vectors["clusters"] = kmeans.labels_
            #print(data["clusters"])
            sse[k] = kmeans.inertia_ # Inertia: Sum of distances of samples to their closest cluster center
        plt.figure()
        plt.plot(list(sse.keys()), list(sse.values()))
        plt.xlabel("Número de Clusters")
        plt.ylabel("Função de Custo (SSE)")
        st.pyplot()
        
    else:
        if model=='kmeans':
            kmeans = KMeans(n_clusters=int(num_clusters), random_state=0)
            clusters=kmeans.fit_predict(df_vectors.values)
            df_vectors['clusters'] =clusters
            df_words=df_vectors.reset_index()[['index','clusters']]
            df_wordcloud=df_words.groupby(['clusters'])['index'].apply(lambda x: ','.join(x)).reset_index()
            
        elif model=='dbscan':

            dbscan = DBSCAN(eps=float(value_eps), min_samples=int(min_samples),metric=metric_distance)
            clusters=dbscan.fit_predict(df_vectors.values)     
            df_vectors['clusters'] =clusters
            df_words=df_vectors.reset_index()[['index','clusters']]
            df_wordcloud=df_words.groupby(['clusters'])['index'].apply(lambda x: ','.join(x)).reset_index()
        
        return df_wordcloud
def visualize_wordcloud(df_wordcloud):
    
    for i,words_index in enumerate(df_wordcloud['index']):
        st.text(f"Cluster {i}")
        wordcloud = WordCloud(background_color='black', width=1600,                            
                            height=800).generate(words_index)
        fig, ax = plt.subplots(figsize=(16,8))            
        ax.imshow(wordcloud, interpolation='bilinear')       
        ax.set_axis_off()
        plt.imshow(wordcloud)
        st.pyplot(fig)

def page_homepage(df):
    st.text("Explore os Dados")
    st.write(df)
    create_wordcloud(df,True)

def page_wordcloud(df):
    ext_features = st.selectbox("Escolha o extrator de features", ['tf_idf','count','word2vec'], index=2)
    model = st.selectbox("Escolha o modelo:", ['kmeans','dbscan'], index=0)
    if model=='kmeans':
        
        st.text("Defina os hiperparametros do K-means")
        st.text("Insira a quantidade de Clusters:")
        num_clusters = st.text_input('Número de clusters',4)
    elif model=='dbscan':
        st.text("Defina os hiperparametros do DBScan")
        value_eps = st.text_input('Valor eps',0.1)
        min_samples = st.text_input('Número mínimo de amostras',5)
        metric_distance = st.selectbox("Métrica de distancia:", ['euclidean','cosine'], index=1)
        num_clusters=0
    
    if st.button('Construir'):

        df_wordcloud = create_wordcloud(df,False,num_clusters,model,ext_features,value_eps,min_samples,metric_distance)
        st.header("Resultados do Agrupamento")
        st.text("Explore os Clusters")
        df_wordcloud
        # Display the generated image:
        st.subheader("Word Cloud por Cluster")
        visualize_wordcloud(df_wordcloud)


def main():
    st.title("Word Cloud - Teste")
    st.text("Ambiente de testes para construção de word cloud")
    uploaded_file = st.file_uploader("Carregar arquivo", type = 'csv')
    page = st.sidebar.selectbox("Menu", ["Home", "Word Cloud"])
    
    
    if uploaded_file is not None:  
        df=load_data(uploaded_file)
        #df = dataprep(df)

        if page == "Home":
            page_homepage(df)


        elif page == "Word Cloud": 
            page_wordcloud(df)




if __name__ == "__main__":
    main()
