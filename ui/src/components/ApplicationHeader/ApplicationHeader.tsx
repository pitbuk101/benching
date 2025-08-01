import { Path } from '@/utils/enum';
import Image from 'next/image';
import Link from 'next/link';

const ApplicationHeader = () => {
  return (
    <div className="header">
      <div className="header-left">
        <Image
          src={'/images/logo.png'}
          alt="logo"
          fill={false}
          height={30}
          width={30}
        />
        <p className="separator">/</p>
        <p className="title">SourceAI</p>
      </div>
      <div className="header-right">
        <Link href={Path.Home} className="admin-link">
          Admin
        </Link>
        <div className="avatar-container">
          <svg
            className="avatar-icon"
            fill="currentColor"
            viewBox="0 0 20 20"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              fillRule="evenodd"
              d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z"
              clipRule="evenodd"
            ></path>
          </svg>
        </div>
      </div>
    </div>
  );
};

export default ApplicationHeader;
