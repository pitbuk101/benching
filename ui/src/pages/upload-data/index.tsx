import AppSidebar from '@/components/AppSidebar/AppSidebar';
import Upload from '@/components/Upload/Upload';
import ApplicationHeader from '@/components/ApplicationHeader/ApplicationHeader';

const Idp = () => {
  return (
    <main className="idp-container">
      <div className="idp-wrapper">
        <ApplicationHeader />
        <div className="idp-content">
          <AppSidebar />
          <div className="idp-content-wrapper">
            <Upload />
          </div>
        </div>
      </div>
    </main>
  );
};

export default Idp;
