import { menuItems } from '@/utils/constants';
import { Fragment } from 'react';

const UserManagementSidebar = ({ tab, setTab }) => {
  return (
    <div className="user-management-sidebar">
      {menuItems.map((section) => (
        <Fragment key={section}>
          <div className="nav-section">
            <div
              className={`nav-link ${tab === section ? 'active' : ''}`}
              onClick={() => setTab(section)}
            >
              {section}
            </div>
          </div>
        </Fragment>
      ))}
    </div>
  );
};

export default UserManagementSidebar;
