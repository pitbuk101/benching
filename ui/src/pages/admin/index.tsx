import React, { useState } from 'react';
import SimpleLayout from '@/components/layouts/SimpleLayout';
import styled from 'styled-components';
import UserManagementSidebar from '@/components/UserManagementSidebar/UserManagementSidebar';
import UserManagementContent from '@/components/UserManagementContent/UserManagementContent';

const PageContainer = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
`;

export default function Admin() {
  const [tab, setTab] = useState<string>('Client Onboarding');

  return (
    <SimpleLayout>
      <PageContainer>
        <div className="user-management-layout">
          <UserManagementSidebar tab={tab} setTab={setTab} />
          <UserManagementContent tab={tab} />
        </div>
      </PageContainer>
    </SimpleLayout>
  );
}
