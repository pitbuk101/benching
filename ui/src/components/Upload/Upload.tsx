import { ChangeEvent, useState } from 'react';
import { UploadCloud } from 'lucide-react';
import SingleSelectFilter from '../SingleSelectFilter/SingleSelectFilter';
import { motion } from 'motion/react';
import ErrorField from '../ErrorField/ErrorField';
import Tost from '@/utils/tostify';
import RightFadeIn from '../RightFadeIn/RightFadeIn';

const Upload = () => {
  const [file, setFile] = useState<File>();
  const [customName, setCustomName] = useState('');
  const [template, setTemplate] = useState('1');
  const [error, setError] = useState({
    file: '',
    customName: '',
  });

  const validity = (): [boolean, { file: string; customName: string }] => {
    const errorObj = {
      file: '',
      customName: '',
    };
    if (!customName)
      errorObj.customName = 'Please add a custom name for the dashboard';
    if (!file) errorObj.file = 'Please select a file';

    if (Object.values(errorObj).some((e) => e !== '')) {
      return [false, errorObj];
    }
    return [true, errorObj];
  };

  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    const file = event?.target?.files?.[0];
    setFile(file);
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const [isValid, error] = validity();
    if (!isValid && error) {
      return setError(error);
    }
    console.log(template);
    setError(error);
    Tost.success(
      {
        header: 'Success',
        message: 'Successfully Added',
      },
      {
        autoClose: 1500,
      },
    );
  };

  return (
    <RightFadeIn>
      <div className="upload-container">
        <div className="upload-header">
          <h1>Data Upload (IDP dashboard)</h1>
        </div>
        <form onSubmit={handleSubmit} className="upload-content">
          {/* Step 1: Template Selection */}
          <div className="step">
            <h3>
              <span className="step-number">1</span> Use this template
            </h3>
            <div className="step-content">
              <SingleSelectFilter
                templates={[
                  { id: '1', name: 'Template 1' },
                  { id: '2', name: 'Template 2' },
                  { id: '3', name: 'Template 3' },
                  { id: '4', name: 'Template 4' },
                ]}
                onSelectTemplate={(selectedFilterId) =>
                  setTemplate(selectedFilterId)
                }
              />
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="download-button"
                type="button"
              >
                Download
              </motion.button>
            </div>
          </div>

          {/* Step 2: File Upload */}
          <div className="step">
            <h3>
              <span className="step-number">2</span> Upload data file
            </h3>
            <label className="file-upload">
              <UploadCloud className="upload-icon" />
              <p>
                Drag and drop your file here or{' '}
                <span className="browse-text">browse files</span>
              </p>
              <p className="file-format-info">.csv, max size 30MB</p>
              <input
                type="file"
                accept=".csv"
                className="hidden-input"
                onChange={handleFileChange}
              />
            </label>
            {file && (
              <p className="selected-file">Selected: {file?.name ?? '-'}</p>
            )}
            <ErrorField msg={error?.file} />
          </div>

          {/* Step 3: Custom Name */}
          <div className="step">
            <h3>
              <span className="step-number">3</span> Custom Name
            </h3>
            <input
              placeholder="Custom name"
              value={customName}
              className="custom-input"
              onChange={(e) => setCustomName(e.target.value)}
            />
            <ErrorField msg={error?.customName} />
          </div>

          {/* Actions */}
          <div className="actions">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="submit-button"
            >
              Submit File
            </motion.button>
          </div>
        </form>
      </div>
    </RightFadeIn>
  );
};

export default Upload;
