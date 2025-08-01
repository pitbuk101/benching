import React, { useEffect } from 'react';
import Paper from '@mui/material/Paper';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TablePagination from '@mui/material/TablePagination';
import TableRow from '@mui/material/TableRow';
import Button from '@mui/material/Button';
import styled from 'styled-components';
import { Edit, Delete } from 'styled-icons/material';
import axios from 'axios';

const StyledButton = styled(Button)`
  width: 200px;
  border-radius: 20px;
  cursor: pointer;
`;

interface Column {
  id:
    | 'clientId'
    | 'sapApiLink'
    | 'clientAlias'
    | 'clientName'
    | 'status'
    | 'clientUserEmail'
    | 'snowFlakeStatus'
    | 'actions';
  label: string;
  minWidth?: number;
  align?: 'right';
  format?: (value: number) => string;
}

const columns: readonly Column[] = [
  { id: 'clientId', label: 'Client Id', minWidth: 170 },
  { id: 'sapApiLink', label: 'Sap Api Link', minWidth: 100 },
  {
    id: 'clientAlias',
    label: 'Client Alias',
    minWidth: 170,
    align: 'right',
    format: (value: number) => value.toLocaleString('en-US'),
  },
  {
    id: 'clientName',
    label: 'Client Name',
    minWidth: 170,
    align: 'right',
    format: (value: number) => value.toLocaleString('en-US'),
  },
  {
    id: 'clientUserEmail',
    label: 'Client User Email',
    minWidth: 170,
    align: 'right',
    format: (value: number) => value.toFixed(2),
  },
  {
    id: 'status',
    label: 'Snowflake status',
    minWidth: 170,
    align: 'right',
  },
  {
    id: 'actions',
    label: 'Actions',
    minWidth: 170,
    align: 'right',
  },
];

const ClientList = ({
  setAddNewClient,
  setOpen,
  setopenDeleteDialogBox,
  setClientIdToEdit,
  setClientIdToDelete,
  rows,
  setRows,
}) => {
  const [page, setPage] = React.useState(0);
  const [rowsPerPage, setRowsPerPage] = React.useState(10);

  useEffect(() => {
    (async () => {
      const token = sessionStorage.getItem('_mid-access-token');
      const clientsResponse = await axios.get(
        `${process.env.NEXT_PUBLIC_ADMIN_END_POINT}/clients`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        },
      );
      setRows(clientsResponse.data);
    })();
  }, []);

  const handleChangePage = (_: unknown, newPage: number) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (
    event: React.ChangeEvent<HTMLInputElement>,
  ) => {
    setRowsPerPage(+event.target.value);
    setPage(0);
  };

  const updateClientIdToEdit = (_data) => {
    setClientIdToEdit(_data);
  };

  const handleEdit = (id) => {
    setOpen(true);
    updateClientIdToEdit(id);
  };

  const handleDelete = (id) => {
    setopenDeleteDialogBox(true);
    setClientIdToDelete(id);
  };

  return (
    <>
      <div className="d-flex justify-content-end mt-4 mb-4">
        <StyledButton variant="contained" onClick={() => setAddNewClient(true)}>
          Add a new Client
        </StyledButton>
      </div>
      <Paper sx={{ width: '100%', overflow: 'hidden' }}>
        <TableContainer sx={{ maxHeight: 440 }}>
          <Table stickyHeader aria-label="sticky table">
            <TableHead>
              <TableRow>
                {columns.map((column) => (
                  <TableCell
                    key={column.id}
                    align={column.align}
                    style={{ minWidth: column.minWidth }}
                  >
                    {column.label}
                  </TableCell>
                ))}
              </TableRow>
            </TableHead>
            <TableBody>
              {rows
                .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                .map((row) => {
                  return (
                    <TableRow hover tabIndex={-1} key={row.clientId}>
                      {columns.map((column) => {
                        const value = row[column.id];
                        return (
                          <TableCell key={column.id} align={column.align}>
                            {column.id === 'actions' ? (
                              <div className="d-flex gap-5 justify-content-end">
                                <Edit
                                  size="24"
                                  className="cursor-pointer action-icons"
                                  onClick={() => handleEdit(row.clientId)}
                                />
                                <Delete
                                  size="24"
                                  className="cursor-pointer action-icons"
                                  onClick={() => handleDelete(row.clientId)}
                                />
                              </div>
                            ) : (
                              value || 'NA'
                            )}
                          </TableCell>
                        );
                      })}
                    </TableRow>
                  );
                })}
            </TableBody>
          </Table>
        </TableContainer>
        <TablePagination
          rowsPerPageOptions={[10, 25, 100]}
          component="div"
          count={rows.length}
          rowsPerPage={rowsPerPage}
          page={page}
          onPageChange={handleChangePage}
          onRowsPerPageChange={handleChangeRowsPerPage}
        />
      </Paper>
    </>
  );
};

export default ClientList;
