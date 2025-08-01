import { ApolloClient, HttpLink, InMemoryCache, from } from '@apollo/client';
import { onError } from '@apollo/client/link/error';
import errorHandler from '@/utils/errorHandler';

const apolloErrorLink = onError((error) => errorHandler(error));

const createApolloClient = (token) => {
  const httpLink = new HttpLink({
    uri: '/api/graphql',
    headers: token
      ? {
          Authorization: `Bearer ${token}`,
        }
      : {},
  });
  const client = new ApolloClient({
    link: from([apolloErrorLink, httpLink]),
    cache: new InMemoryCache(),
  });
  return client;
};

export default createApolloClient;
