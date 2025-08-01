import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import { Button, Layout, Space } from 'antd';
import styled from 'styled-components';
import { Path } from '@/utils/enum';
import Deploy from '@/components/deploy/Deploy';
import MenuItem from '@mui/material/MenuItem';
import Select from '@mui/material/Select';
import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';
import axios from 'axios';
import { ClientIdContextConsumer } from '@/context/ClientIdContext';

const { Header } = Layout;

const StyledButton = styled(Button)<{ $isHighlight: boolean }>`
  background: ${(props) =>
    props.$isHighlight ? 'rgba(255, 255, 255, 0.20)' : 'transparent'};
  font-weight: ${(props) => (props.$isHighlight ? '700' : 'normal')};
  border: none;
  color: var(--gray-1);

  &:hover,
  &:focus {
    background: ${(props) =>
      props.$isHighlight
        ? 'rgba(255, 255, 255, 0.20)'
        : 'rgba(255, 255, 255, 0.05)'};
    color: var(--gray-1);
  }
`;

const StyledHeader = styled(Header)`
  min-height: 77px;
  border-bottom: 1px solid var(--gray-5);
  background: var(--gray-10);
  padding: 10px 16px;
  disolay: flex;
  justify-content: space-between;
  align-items: center;
`;

const LogoText = styled.span`
  height: 48px;
  color: #fff;
  padding: 10px 16px;
  font-size: 20px;
`;

export default function HeaderBar() {
  const router = useRouter();
  const { pathname } = router;
  const showNav = !pathname.startsWith(Path.Onboarding);
  const isModeling = pathname.startsWith(Path.Modeling);
  const [clientData, setClientData] = useState([]);

  const handleClientChange = (event: any, setClientId: any) => {
    setClientId(event.target.value as string);
  };

  useEffect(() => {
    (async () => {
      const token = sessionStorage.getItem('_mid-access-token');
      const clientData = await axios.get(
        `${process.env.NEXT_PUBLIC_ADMIN_END_POINT}/clients`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        },
      );
      setClientData(clientData.data);
    })();
  }, []);

  return (
    <StyledHeader>
      <div className="d-flex justify-space-between align-center">
        <div
          className="d-flex justify-space-between align-center"
          style={{ marginTop: -2 }}
        >
          <Space size={[48, 0]}>
            <LogoText>SAI KF Chatbot Dev</LogoText>
            {showNav && (
              <Space size={[16, 0]}>
                <StyledButton
                  shape="round"
                  size="small"
                  $isHighlight={pathname.startsWith(Path.Home)}
                  onClick={() => router.push(Path.Home)}
                >
                  Home
                </StyledButton>
                <StyledButton
                  shape="round"
                  size="small"
                  $isHighlight={pathname.startsWith(Path.Modeling)}
                  onClick={() => router.push(Path.Modeling)}
                >
                  Modeling
                </StyledButton>
                <StyledButton
                  shape="round"
                  size="small"
                  $isHighlight={pathname.startsWith(Path.Admin)}
                  onClick={() => router.push(Path.Admin)}
                >
                  Admin
                </StyledButton>
                <StyledButton
                  shape="round"
                  size="small"
                  $isHighlight={pathname.startsWith(Path.idp)}
                  onClick={() => router.push(Path.idp)}
                >
                  IDP
                </StyledButton>
              </Space>
            )}
          </Space>
          {isModeling && (
            <Space size={[16, 0]}>
              <Deploy />
            </Space>
          )}
        </div>
        <div className="d-flex align-center gap-2">
          <ClientIdContextConsumer>
            {(value) => (
              <FormControl
                sx={{ m: 1, minWidth: 120 }}
                size="small"
                className="client-select-div select-form-control-div"
              >
                <InputLabel
                  id="demo-select-small-label"
                  className="color-white"
                >
                  Client
                </InputLabel>
                <Select
                  labelId="demo-select-small-label"
                  id="demo-select-small"
                  value={value.currentClient}
                  label="Age"
                  onChange={(e) =>
                    handleClientChange(e, value.setCurrentClient)
                  }
                  className="color-white"
                >
                  {clientData.map((client) => {
                    return (
                      <MenuItem key={client.clientId} value={client.clientId}>
                        {client.clientAlias}
                      </MenuItem>
                    );
                  })}
                </Select>
              </FormControl>
            )}
          </ClientIdContextConsumer>
          <Button>Change Client</Button>
        </div>
      </div>
    </StyledHeader>
  );
}
