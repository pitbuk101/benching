import React, { useState } from 'react';
import styled from 'styled-components';
import Collapse from '@mui/material/Collapse';
import ClientOnboarding from '@/components/Client/ClientOnboarding';
import ClientList from '@/components/Client/ClientList';
import EditClient from '@/components/Client/EditClient';
import DeleteClientConfirmationModal from '@/components/Client/DeleteClientConfirmationModal';

const PageContainer = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
`;

export default function Client() {
  const [addNewClient, setAddNewClient] = useState(false);
  const [openEditDialogBox, setOpenEditDialogBox] = useState(false);
  const [rows, setRows] = React.useState([]);
  const [openDeleteDialogBox, setopenDeleteDialogBox] = useState(false);
  const [clientIdToEdit, setClientIdToEdit] = useState('');
  const [clientIdToDelete, setClientIdToDelete] = useState('');

  const [formData, setFormData] = useState({
    sapApiLink: '',
    clientAlias: '',
    clientName: '',
    clientUserEmail: '',
    clientTenantId: '',
  });

  const [errors, setErrors] = useState({
    sapApiLink: '',
    clientAlias: '',
    clientName: '',
    clientUserEmail: '',
    clientTenantId: '',
  });

  return (
    <PageContainer>
      <div className="d-flex flex-column justify-content-center w-95">
        <Collapse in={!addNewClient} className="client-list-collapsable">
          <ClientList
            setAddNewClient={setAddNewClient}
            setOpen={setOpenEditDialogBox}
            setopenDeleteDialogBox={setopenDeleteDialogBox}
            setClientIdToEdit={setClientIdToEdit}
            setClientIdToDelete={setClientIdToDelete}
            rows={rows}
            setRows={setRows}
          />
        </Collapse>
        <Collapse in={addNewClient} className="client-onboarding-collapsable">
          <ClientOnboarding
            formData={formData}
            setFormData={setFormData}
            errors={errors}
            setErrors={setErrors}
            setAddNewClient={setAddNewClient}
            rows={rows}
            setRows={setRows}
          />
        </Collapse>
      </div>
      <EditClient
        open={openEditDialogBox}
        setOpen={setOpenEditDialogBox}
        clientIdToEdit={clientIdToEdit}
        rows={rows}
        setRows={setRows}
      />
      <DeleteClientConfirmationModal
        open={openDeleteDialogBox}
        setOpen={setopenDeleteDialogBox}
        clientIdToDelete={clientIdToDelete}
        rows={rows}
        setRows={setRows}
      />
    </PageContainer>
  );
}
