import { createContext, useContext, useState, useMemo } from 'react';
import { Layout } from 'antd';
import HeaderBar from '@/components/HeaderBar';
import PageLoading from '@/components/PageLoading';
import { useWithOnboarding } from '@/hooks/useCheckOnboarding';

const { Content } = Layout;

type LayoutState = {
  selectedClient: string;
  changeClient: (newState: string) => void;
};

const defaultState: LayoutState = {
  selectedClient: 'Demo',
  changeClient: () => {},
};

const StateContext = createContext<LayoutState>(defaultState);

export const useLayoutState = () => useContext(StateContext);

interface Props {
  readonly children: React.ReactNode;
  readonly loading?: boolean;
}

export default function SimpleLayout(props: Props) {
  const [selectedClient, setSelectedClient] = useState('Demo');

  const changeClient = (newState: string) => {
    setSelectedClient(newState);
  };

  const contextValue = useMemo(
    () => ({ selectedClient, changeClient }),
    [selectedClient],
  );

  const { loading: fetching } = useWithOnboarding();
  const { children, loading } = props;
  const pageLoading = fetching || loading;
  return (
    <StateContext.Provider value={contextValue}>
      <Layout
        className={`adm-main bg-gray-3${pageLoading ? ' overflow-hidden' : ''}`}
      >
        <HeaderBar />
        <Content className="adm-content">{children}</Content>
        <PageLoading visible={pageLoading} />
      </Layout>
    </StateContext.Provider>
  );
}
