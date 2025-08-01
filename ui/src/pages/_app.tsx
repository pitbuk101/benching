import { AppProps } from 'next/app';
import Head from 'next/head';
import { Spin } from 'antd';
import createApolloClient from '@/apollo/client';
import { ApolloProvider } from '@apollo/client';
import { defaultIndicator } from '@/components/PageLoading';
import { buildMid } from './api/mck-id';
import MckId from './mck-id';
import { useEffect, useState } from 'react';
import { ClientIdContextProvider } from '../context/ClientIdContext';
import '../styles/global.css';
import { ToastContainer, Bounce } from 'react-toastify';
require('../styles/index.less');

Spin.setDefaultIndicator(defaultIndicator);

function App({ Component, pageProps }: AppProps) {
  const [token, setToken] = useState<string | null>(null);
  const [currentClient, setCurrentClient] = useState<any>('Demo');

  useEffect(() => {
    const storedToken = sessionStorage.getItem('_mid-access-token');
    setToken(storedToken);
  }, []);

  return (
    <>
      <Head>
        <title>Wren AI</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <MckId mid={buildMid()}>
        <ApolloProvider client={createApolloClient(token)}>
          <ClientIdContextProvider value={{ currentClient, setCurrentClient }}>
            <main className="app">
              <ToastContainer
                position="top-right"
                autoClose={5000}
                hideProgressBar={false}
                newestOnTop={false}
                closeOnClick={false}
                rtl={false}
                pauseOnFocusLoss
                draggable
                pauseOnHover
                theme="dark"
                transition={Bounce}
              />
              <Component {...pageProps} />
            </main>
          </ClientIdContextProvider>
        </ApolloProvider>
      </MckId>
    </>
  );
}

export default App;
