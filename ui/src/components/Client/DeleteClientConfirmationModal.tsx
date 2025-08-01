import React from 'react';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import Button from '@mui/material/Button';
import axios from 'axios';

const DeleteClientConfirmationModal = ({
  open,
  setOpen,
  clientIdToDelete,
  rows,
  setRows,
}) => {
  const handleDelete = () => {
    (async () => {
      const token = sessionStorage.getItem('_mid-access-token');
      const delRes = await axios.delete(
        `${process.env.NEXT_PUBLIC_ADMIN_END_POINT}/clients/${clientIdToDelete}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        },
      );
      setOpen(false);
      if (delRes.status === 200) {
        let temp = rows;
        temp = temp.filter((item) => item.clientId !== clientIdToDelete);
        setRows(temp);
      }
    })();
  };

  const handleClose = () => {
    setOpen(false);
  };

  return (
    <Dialog
      open={open}
      onClose={handleClose}
      aria-labelledby="alert-dialog-title"
      aria-describedby="alert-dialog-description"
    >
      <DialogContent>
        <DialogContentText id="alert-dialog-description">
          Are you sure, you want to delete this client ?
        </DialogContentText>
      </DialogContent>
      <DialogActions>
        <Button onClick={() => setOpen(false)}>Cancel</Button>
        <Button autoFocus onClick={handleDelete}>
          Confirm
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default DeleteClientConfirmationModal;
