import { Fragment } from 'react';
import { Upload, Radar } from 'lucide-react';
import { usePathname } from 'next/navigation';
import ViewTransitionLink from '../ViewTransitionLink/ViewTransitionLink';

// Sidebar menu structure
const menuItems = [
  {
    showGroupName: false,
    group: 'Home',
    child: [{ name: 'Data Upload', Icon: Upload, to: '/upload-data' }],
  },
  {
    showGroupName: true,
    group: 'Smart On',
    child: [{ name: 'IDP Dashboard', Icon: Radar, to: '/idp-dashboard' }],
  },
];

const DashboardSidebar = () => {
  const pathname = usePathname();

  return (
    <aside className="sidebar">
      <div className="sidebar-container">
        <nav className="nav">
          {menuItems.map((section) => (
            <Fragment key={section.group}>
              {section.showGroupName && (
                <div className="nav-header">{section.group}</div>
              )}
              {section.child.map(({ name, Icon, to }) => (
                <div key={name} className="nav-section">
                  <ViewTransitionLink
                    to={to}
                    className={`nav-link ${pathname === to ? 'active' : ''}`}
                  >
                    <Icon
                      className={`icon ${pathname === to ? 'active-icon' : ''} link-icon`}
                    />
                    {name}
                  </ViewTransitionLink>
                </div>
              ))}
            </Fragment>
          ))}
        </nav>
      </div>
    </aside>
  );
};

export default DashboardSidebar;
