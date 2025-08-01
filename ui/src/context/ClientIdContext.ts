import { createContext } from 'react';

interface MyContextType {
  currentClient: string;
  setCurrentClient: (state: string) => void;
}

const defaultContextValue: MyContextType = {
  currentClient: 'Demo',
  setCurrentClient: () => {},
};

const ClientIdContext = createContext<MyContextType>(defaultContextValue);

export const ClientIdContextProvider = ClientIdContext.Provider;
export const ClientIdContextConsumer = ClientIdContext.Consumer;
