import React, { useState } from 'react';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import styled from 'styled-components';
import { LinearProgress } from '@mui/material';
import axios from 'axios';
import Collapse from '@mui/material/Collapse';
import Zoom from '@mui/material/Zoom';
import { Check, Cancel } from 'styled-icons/material';

const FormContainer = styled.div`
  background-color: white;
  padding: 20px 40px;
  border-radius: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 500px; /* Max width to avoid form becoming too large */
`;

const FormTitle = styled.h2`
  text-align: center;
  margin-bottom: 20px;
  color: #333;
`;

const Form = styled.form`
  display: flex;
  flex-direction: column;
  gap: 20px;
`;

const StyledTextField = styled(TextField)`
  & .MuiInputBase-root {
    height: 50px;
  }
`;

const StyledButtonContainer = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
`;

const StyledButton = styled(Button)`
  width: 200px;
  border-radius: 20px;
  cursor: pointer;
`;

const ProgressWrapper = styled.div`
  width: 100%;
  margin-top: 16px;
`;

const ProgressText = styled.span`
  font-size: 14px;
  color: #333;
`;

const ClientOnboarding = ({
  formData,
  setFormData,
  errors,
  setErrors,
  setAddNewClient,
  rows,
  setRows,
}) => {
  const [loading, setLoading] = useState(false);
  const [postgresProgress, setPostgresProgress] = useState(0);
  const [showPostgresProgress, setShowPostgresProgress] = useState(false);
  const [postgresProgressComplete, setPostgresProgressComplete] =
    useState(false);
  const [databaseCreatedSuccessfully, setDatabaseCreatedSuccessfully] =
    useState(false);

  const handleInputChange = (e) => {
    const { id, value } = e.target;
    setFormData((prevState) => ({
      ...prevState,
      [id]: value,
    }));
  };

  const resetForm = () => {
    setFormData({
      sapApiLink: '',
      clientAlias: '',
      clientName: '',
      clientUserEmail: '',
    });
    setPostgresProgressComplete(false);
    setShowPostgresProgress(false);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    // Reset errors
    const formErrors = { ...errors };

    // Validation checks
    if (!formData.sapApiLink) {
      formErrors.sapApiLink = 'Sap Api Link is required';
    } else {
      formErrors.sapApiLink = '';
    }

    if (!formData.clientAlias) {
      formErrors.clientAlias = 'Client Alias is required';
    } else {
      formErrors.clientAlias = '';
    }

    if (!formData.clientName) {
      formErrors.clientName = 'Client Name is required';
    } else {
      formErrors.clientName = '';
    }

    formErrors.clientUserEmail = '';
    setErrors(formErrors);

    // Check if there are no errors before submitting the form
    const isValid = !Object.values(formErrors).some((error) => error !== '');

    if (isValid) {
      setShowPostgresProgress(true);
      try {
        const token = sessionStorage.getItem('_mid-access-token');
        const response = await axios.post(
          `${process.env.CLIENT_ONBORDING_END_POINT}/create-client`,
          {
            sap_api_link: formData.sapApiLink,
            client_alias: formData.clientAlias,
            client_name: formData.clientName,
            client_user_email: formData.clientUserEmail,
            client_id: formData.clientTenantId?.trim() || undefined,
          },
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
            onUploadProgress: (progressEvent) => {
              const { loaded, total } = progressEvent;
              const percentCompleted = Math.floor((loaded * 100) / total);
              setPostgresProgress(percentCompleted);
              setPostgresProgressComplete(true);
            },
          },
        );
        if (response.status === 201) setDatabaseCreatedSuccessfully(true);
        setRows([
          ...rows,
          {
            clientId: response.data.client.clientId,
            sapApiLink: response.data.client.sapApiLink,
            clientAlias: response.data.client.clientAlias,
            clientName: response.data.client.clientName,
            clientUserEmail: response.data.client.clientUserEmail || '',
          },
        ]);
        setLoading(false);
      } catch (error) {
        console.error('Error submitting form:', error);
        setLoading(false);
      }
    } else {
      setLoading(false);
    }
  };

  return (
    <>
      <div className="d-flex justify-content-end mt-4 mb-4">
        <StyledButton
          variant="contained"
          onClick={() => setAddNewClient(false)}
        >
          Back to client list
        </StyledButton>
      </div>
      <div className="flex-center">
        <FormContainer>
          <FormTitle>Client Onboarding</FormTitle>
          <Form>
            <StyledTextField
              error={!!errors.sapApiLink}
              id="sapApiLink"
              label="SAP Api Link *"
              variant="outlined"
              value={formData.sapApiLink}
              onChange={handleInputChange}
            />
            <StyledTextField
              error={!!errors.clientAlias}
              id="clientAlias"
              label="Client Alias *"
              variant="outlined"
              value={formData.clientAlias}
              onChange={handleInputChange}
            />
            <StyledTextField
              error={!!errors.clientName}
              id="clientName"
              label="Client Name *"
              variant="outlined"
              value={formData.clientName}
              onChange={handleInputChange}
            />
            <StyledTextField
              id="clientUserEmail"
              label="Client User Email"
              variant="outlined"
              value={formData.clientUserEmail}
              onChange={handleInputChange}
            />
            <StyledTextField
              id="clientTenantId"
              label="Client Tenant Id"
              variant="outlined"
              value={formData.clientTenantId}
              onChange={handleInputChange}
            />
            <StyledButtonContainer>
              <StyledButton
                variant="contained"
                loading={loading}
                onClick={postgresProgressComplete ? resetForm : handleSubmit}
              >
                {postgresProgressComplete
                  ? 'Reset Form'
                  : 'Initiate Onboarding'}
              </StyledButton>
            </StyledButtonContainer>
            <Collapse in={showPostgresProgress}>
              <ProgressWrapper>
                <div
                  style={{ display: 'flex', justifyContent: 'space-between' }}
                >
                  <ProgressText>Setting up database...</ProgressText>
                  <Zoom in={postgresProgressComplete}>
                    {databaseCreatedSuccessfully ? (
                      <Check size={24} color={'green'} />
                    ) : (
                      <Cancel size={24} color={'red'} />
                    )}
                  </Zoom>
                </div>
                <LinearProgress
                  variant="determinate"
                  value={postgresProgress}
                  style={{
                    transition: 'width 0.2s ease-in-out',
                    marginTop: '16px',
                  }}
                />
              </ProgressWrapper>
            </Collapse>
          </Form>
        </FormContainer>
      </div>
    </>
  );
};

export default ClientOnboarding;
