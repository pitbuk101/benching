import React, { useState, useEffect } from 'react';
import Button from '@mui/material/Button';
import { styled } from '@mui/material/styles';
import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';
import DialogActions from '@mui/material/DialogActions';
import IconButton from '@mui/material/IconButton';
import TextField from '@mui/material/TextField';
import axios from 'axios';

const BootstrapDialog = styled(Dialog)(({ theme }) => ({
  '& .MuiDialogContent-root': {
    padding: theme.spacing(2),
  },
  '& .MuiDialogActions-root': {
    padding: theme.spacing(1),
  },
}));

const StyledTextField = styled(TextField)`
  & .MuiInputBase-root {
    height: 50px;
  }
`;

const EditClient = ({ open, setOpen, clientIdToEdit, rows, setRows }) => {
  const [formData, setFormData] = useState({
    sapApiLink: '',
    clientAlias: '',
    clientName: '',
    clientUserEmail: '',
  });

  useEffect(() => {
    (async () => {
      if (clientIdToEdit !== '') {
        const token = sessionStorage.getItem('_mid-access-token');
        const clientData = await axios.get(
          `${process.env.NEXT_PUBLIC_ADMIN_END_POINT}/clients/${clientIdToEdit}`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          },
        );
        setFormData(clientData.data);
      }
    })();
  }, [clientIdToEdit]);

  const handleClose = () => {
    setOpen(false);
  };

  const handleEdit = async () => {
    const token = sessionStorage.getItem('_mid-access-token');
    const editRes = await axios.put(
      `${process.env.NEXT_PUBLIC_ADMIN_END_POINT}/clients/${clientIdToEdit}`,
      formData,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      },
    );
    if (editRes.status === 200) {
      const temp = rows.map((row) =>
        row.clientId === clientIdToEdit ? { ...row, ...formData } : row,
      );
      setRows(temp);
      handleClose();
    }
  };

  const handleInputChange = (e) => {
    const { id, value } = e.target;
    setFormData((prevState) => ({
      ...prevState,
      [id]: value,
    }));
  };

  return (
    <BootstrapDialog
      onClose={handleClose}
      aria-labelledby="customized-dialog-title"
      open={open}
    >
      <DialogTitle sx={{ m: 0, p: 2 }} id="customized-dialog-title">
        Edit Client info
      </DialogTitle>
      <IconButton
        aria-label="close"
        onClick={handleClose}
        sx={(theme) => ({
          position: 'absolute',
          right: 8,
          top: 8,
          color: theme.palette.grey[500],
        })}
      >
        Close
      </IconButton>
      <DialogContent dividers>
        <div className="flex-center flex-column gap-10">
          <StyledTextField
            // error={!!errors.sapApiLink}
            id="sapApiLink"
            label="SAP Api Link *"
            variant="outlined"
            value={formData.sapApiLink}
            onChange={handleInputChange}
          />
          <StyledTextField
            // error={!!errors.clientAlias}
            id="clientAlias"
            label="Client Alias *"
            variant="outlined"
            value={formData.clientAlias}
            onChange={handleInputChange}
          />
          <StyledTextField
            // error={!!errors.clientName}
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
        </div>
      </DialogContent>
      <DialogActions>
        <Button autoFocus onClick={handleEdit}>
          Save changes
        </Button>
      </DialogActions>
    </BootstrapDialog>
  );
};

export default EditClient;
