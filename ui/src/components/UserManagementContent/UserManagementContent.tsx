import Client from '@/pages/client';
import AddUser from '../AddUser/AddUser';
import RoleDetails from '../RoleDetails/RoleDetails';
import SaiConfig from '../SAIconfig/SAIconfig';
import MarketRadar from '../MarketRadar/MarketRadar';

const UserManagementContent = ({ tab }) => {
  let content;

  switch (tab) {
    case 'Client Onboarding':
      content = <Client />;
      break;
    case 'User Management':
      content = <AddUser />;
      break;
    case 'Role Details':
      content = <RoleDetails />;
      break;
    case 'Market Radar':
      content = <MarketRadar />;
      break;
    case 'SourceAI Configuration':
      content = <SaiConfig />;
      break;
    default:
    // content = <Client />;
  }

  return <div className="user-management-content">{content}</div>;
};

export default UserManagementContent;
