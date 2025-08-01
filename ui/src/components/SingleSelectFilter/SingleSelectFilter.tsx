import { useState } from 'react';

const SingleSelectFilter = ({
  templates = [],
  onSelectTemplate,
}: {
  templates: any;
  onSelectTemplate: any;
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedTemplate, setSelectedTemplate] = useState(
    templates[0] || { id: '1', name: 'Template 1' },
  );

  const handleToggleDropdown = () => {
    setIsOpen(!isOpen);
  };

  const handleSelectTemplate = (template: any) => {
    setSelectedTemplate(template);
    setIsOpen(false);
    if (onSelectTemplate) {
      onSelectTemplate(template);
    }
  };

  return (
    <div className="template-select-container">
      {/* Dropdown trigger */}
      <button
        style={{ inset: 'unset', width: '100%' }}
        className="template-select-trigger"
        onClick={handleToggleDropdown}
        type="button"
      >
        <span className="template-select-value">{selectedTemplate.name}</span>
        <span className="template-select-icon">
          {isOpen ? (
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <polyline points="18 15 12 9 6 15"></polyline>
            </svg>
          ) : (
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <polyline points="6 9 12 15 18 9"></polyline>
            </svg>
          )}
        </span>
      </button>

      {/* Dropdown content */}
      {isOpen && (
        <div className="template-select-dropdown">
          <ul className="template-select-options">
            {(templates.length > 0
              ? templates
              : [
                  { id: '1', name: 'Template 1' },
                  { id: '2', name: 'Template 2' },
                  { id: '3', name: 'Template 3' },
                  { id: '4', name: 'Template 4' },
                ]
            ).map((template) => (
              <button
                key={template.id}
                style={{ inset: 'unset', width: '100%' }}
                className={`template-select-option ${selectedTemplate.id === template.id ? 'selected' : ''}`}
                onClick={() => handleSelectTemplate(template)}
              >
                <div className="template-radio">
                  <div
                    className={`radio-circle ${selectedTemplate.id === template.id ? 'checked' : ''}`}
                  >
                    {selectedTemplate.id === template.id && (
                      <div className="radio-inner"></div>
                    )}
                  </div>
                </div>
                <span className="template-name">{template.name}</span>
                {selectedTemplate.id === template.id && (
                  <span className="checkmark">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="20"
                      height="20"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    >
                      <polyline points="20 6 9 17 4 12"></polyline>
                    </svg>
                  </span>
                )}
              </button>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default SingleSelectFilter;
