import { useState, useEffect } from 'react';
import styled from 'styled-components';
import {
  Typography,
  TextField,
  Button,
  CircularProgress,
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  IconButton,
  MenuItem,
} from '@mui/material';
import { Delete as DeleteIcon } from '@styled-icons/material/Delete';
import { UploadFile as UploadFileIcon } from '@styled-icons/material/UploadFile';

const Container = styled.div`
  max-width: 1200px;
  margin: 40px auto;
  padding: 30px;
  background-color: #fafafa;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  gap: 24px;
`;

const HeaderRow = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const ClientFieldsColumn = styled.div`
  display: flex;
  flex-direction: column;
  gap: 16px;
  width: 100%;

  .MuiFormControl-root,
  .MuiTextField-root {
    min-height: 56px;
  }

  .MuiInputBase-root {
    min-height: 56px;
    display: flex;
    align-items: center;
  }
`;

const FieldWrapper = styled.div`
  width: 100%;
`;

const ScrollableTableWrapper = styled.div`
  overflow-x: auto;
  width: 100%;
  table {
    border-collapse: collapse;
  }
`;

const RequiredLabel = styled.span`
  color: red;
  margin-left: 2px;
`;

const SectionHeader = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
`;

const StyledTableCell = styled(TableCell)`
  min-width: 200px;
  padding: 6px 12px;
  border: 1px solid #ddd;
  &.MuiTableCell-head {
    font-weight: 700;
    font-size: 1.1rem;
    background-color: #f5f5f5;
  }
`;

const FileUploadSection = styled.div`
  display: flex;
  gap: 16px;
`;

const DropZone = styled.div<{ isDragging: boolean; hasError: boolean }>`
  flex: 1;
  border: 2px dashed ${({ hasError }) => (hasError ? 'red' : '#ccc')};
  border-radius: 8px;
  padding: 20px;
  cursor: pointer;
  background-color: ${({ isDragging }) =>
    isDragging ? '#e3f2fd' : 'transparent'};
  transition: background-color 0.2s ease;
  min-height: 140px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
`;

const ButtonsRow = styled.div`
  display: flex;
  gap: 12px;
  margin-top: 24px;
`;

type Client = {
  clientId: string;
  clientName: string;
};

const MarketRadar = () => {
  const [clientId, setClientId] = useState('');
  const [clientName, setClientName] = useState('');
  const [clients, setClients] = useState<Client[]>([]);
  const [supplierFile, setSupplierFile] = useState<File | null>(null);
  const [keywordFile, setKeywordFile] = useState<File | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [, setSubmitted] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [fieldErrors, setFieldErrors] = useState<{
    clientId?: boolean;
    clientName?: boolean;
    supplierFile?: boolean;
    keywordFile?: boolean;
  }>({});

  const [useUpload, setUseUpload] = useState(true);

  const supplierColumns = [
    'industry',
    'custom_topic_id',
    'id',
    'name',
    'description',
    'source_name',
    'url',
    'country',
    'alternative_name',
    'advancedQuery',
    'category_id',
  ];
  const keywordColumns = [
    'id',
    'custom_topic_id',
    'name',
    'type',
    'category_id',
    'advancedQuery',
    'category_name',
  ];

  const [supplierRows, setSupplierRows] = useState<any[]>([]);
  const [keywordRows, setKeywordRows] = useState<any[]>([]);

  useEffect(() => {
    const fetchClients = async () => {
      try {
        const res = await fetch(
          `${process.env.ADMIN_MARKET_RADAR_END_POINT}/all-clients`,
        );
        if (!res.ok) throw new Error('Failed to fetch clients');
        const data: Client[] = await res.json();
        setClients(data);
      } catch (err) {
        console.error(err);
        setError('Failed to load clients.');
      }
    };
    fetchClients();
  }, []);

  useEffect(() => {
    const selected = clients.find((c) => c.clientId === clientId);
    setClientName(selected ? selected.clientName : '');
  }, [clientId, clients]);

  const isJsonFile = (file: File | null) =>
    !!file &&
    file.name.toLowerCase().endsWith('.json') &&
    file.type === 'application/json';

  const handleFileChange = (
    type: 'supplier' | 'keyword',
    file: File | null,
  ) => {
    setError(null);
    if (file && !isJsonFile(file)) {
      setError('Only JSON files allowed.');
      setFieldErrors((fe) => ({
        ...fe,
        [type + 'File']: true,
      }));
      if (type === 'supplier') setSupplierFile(null);
      else setKeywordFile(null);
      return;
    }
    if (type === 'supplier') {
      setSupplierFile(file);
      setFieldErrors((fe) => ({ ...fe, supplierFile: false }));
    } else {
      setKeywordFile(file);
      setFieldErrors((fe) => ({ ...fe, keywordFile: false }));
    }
  };

  const [draggingSupplier, setDraggingSupplier] = useState(false);
  const [draggingKeyword, setDraggingKeyword] = useState(false);

  const handleDragEnter = (type: 'supplier' | 'keyword') => {
    type === 'supplier' ? setDraggingSupplier(true) : setDraggingKeyword(true);
  };
  const handleDragLeave = (type: 'supplier' | 'keyword') => {
    type === 'supplier'
      ? setDraggingSupplier(false)
      : setDraggingKeyword(false);
  };
  const handleDragOver = (e: React.DragEvent) => e.preventDefault();
  const handleDropFile = (type: 'supplier' | 'keyword', e: React.DragEvent) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file) handleFileChange(type, file);
    handleDragLeave(type);
  };

  const validateForm = () => {
    const errs: typeof fieldErrors = {};
    let valid = true;
    if (!clientId.trim()) {
      errs.clientId = true;
      valid = false;
    }
    if (!clientName.trim()) {
      errs.clientName = true;
      valid = false;
    }
    if (useUpload) {
      if (!supplierFile) {
        errs.supplierFile = true;
        valid = false;
      }
      if (!keywordFile) {
        errs.keywordFile = true;
        valid = false;
      }
    }
    setFieldErrors(errs);
    if (valid) setError(null);
    return valid;
  };

  const handleSubmit = async () => {
    if (!validateForm()) return;
    setIsSubmitting(true);
    setError(null);
    try {
      if (useUpload) {
        const fd = new FormData();
        fd.append('client_id', clientId.trim());
        fd.append('client_name', clientName.trim());
        fd.append('supplierConfig', supplierFile as Blob);
        fd.append('keywordConfig', keywordFile as Blob);
        const res = await fetch(
          `${process.env.ADMIN_MARKET_RADAR_END_POINT}/upload-config`,
          {
            method: 'POST',
            body: fd,
          },
        );
        if (!res.ok) {
          const err = await res.json();
          throw new Error(err.message || 'Upload failed');
        }
      } else {
        const res = await fetch(
          `${process.env.ADMIN_MARKET_RADAR_END_POINT}/submit-table-config`,
          {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              client_id: clientId.trim(),
              client_name: clientName.trim(),
              supplierConfig: supplierRows,
              keywordConfig: keywordRows,
            }),
          },
        );
        if (!res.ok) {
          const err = await res.json();
          throw new Error(err.message || 'Submission failed');
        }
      }
      setSubmitted(true);
    } catch (err: any) {
      setError(err.message || 'Something went wrong');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleReset = () => {
    setClientId('');
    setClientName('');
    setSupplierFile(null);
    setKeywordFile(null);
    setSupplierRows([]);
    setKeywordRows([]);
    setError(null);
    setFieldErrors({});
    setSubmitted(false);
    setIsSubmitting(false);
  };

  const addSupplierRow = () => setSupplierRows((r) => [...r, {}]);
  const deleteSupplierRow = (idx: number) =>
    setSupplierRows((r) => r.filter((_, i) => i !== idx));
  const updateSupplierCell = (rowIndex: number, col: string, value: string) => {
    setSupplierRows((rows) =>
      rows.map((row, i) => (i === rowIndex ? { ...row, [col]: value } : row)),
    );
  };

  const addKeywordRow = () => setKeywordRows((r) => [...r, {}]);
  const deleteKeywordRow = (idx: number) =>
    setKeywordRows((r) => r.filter((_, i) => i !== idx));
  const updateKeywordCell = (rowIndex: number, col: string, value: string) => {
    setKeywordRows((rows) =>
      rows.map((row, i) => (i === rowIndex ? { ...row, [col]: value } : row)),
    );
  };

  return (
    <Container>
      <HeaderRow>
        <Typography variant="h4" component="h1">
          Market Radar Configuration
        </Typography>

        <Button
          variant="outlined"
          onClick={() => setUseUpload((v) => !v)}
          size="small"
          sx={{ height: 36 }}
          aria-label="Toggle input mode"
        >
          {useUpload ? 'Switch to Table Edit' : 'Switch to Upload JSON'}
        </Button>
      </HeaderRow>

      <ClientFieldsColumn>
        <FieldWrapper>
          <TextField
            select
            label={
              <>
                Client Id
                <RequiredLabel>*</RequiredLabel>
              </>
            }
            value={clientId}
            onChange={(e) => setClientId(e.target.value)}
            fullWidth
            error={!!fieldErrors.clientId}
            helperText={fieldErrors.clientId && 'Client Id is required'}
            size="small"
          >
            <MenuItem value="">Select client</MenuItem>
            {clients.map((c) => (
              <MenuItem key={c.clientId} value={c.clientId}>
                {c.clientId}
              </MenuItem>
            ))}
          </TextField>
        </FieldWrapper>

        <FieldWrapper>
          <TextField
            label={
              <>
                Client Name
                <RequiredLabel>*</RequiredLabel>
              </>
            }
            value={clientName}
            onChange={(e) => setClientName(e.target.value)}
            fullWidth
            error={!!fieldErrors.clientName}
            helperText={fieldErrors.clientName && 'Client Name is required'}
            size="small"
          />
        </FieldWrapper>
      </ClientFieldsColumn>

      {useUpload ? (
        <FileUploadSection>
          <DropZone
            isDragging={draggingSupplier}
            hasError={!!fieldErrors.supplierFile}
            onDragEnter={() => handleDragEnter('supplier')}
            onDragLeave={() => handleDragLeave('supplier')}
            onDragOver={handleDragOver}
            onDrop={(e) => handleDropFile('supplier', e)}
            onClick={() => document.getElementById('supplier-file')?.click()}
            role="button"
            tabIndex={0}
            aria-label="Upload Supplier JSON File"
          >
            <input
              type="file"
              id="supplier-file"
              accept=".json"
              hidden
              onChange={(e) =>
                handleFileChange('supplier', e.target.files?.[0] || null)
              }
            />
            <UploadFileIcon size="40" />
            <Typography variant="body1" mt={1}>
              Drag & Drop or Click to upload supplier config JSON
            </Typography>
            {supplierFile && (
              <Typography
                variant="body2"
                mt={1}
                color={fieldErrors.supplierFile ? 'error' : 'textPrimary'}
              >
                {supplierFile.name}
              </Typography>
            )}
          </DropZone>

          <DropZone
            isDragging={draggingKeyword}
            hasError={!!fieldErrors.keywordFile}
            onDragEnter={() => handleDragEnter('keyword')}
            onDragLeave={() => handleDragLeave('keyword')}
            onDragOver={handleDragOver}
            onDrop={(e) => handleDropFile('keyword', e)}
            onClick={() => document.getElementById('keyword-file')?.click()}
            role="button"
            tabIndex={0}
            aria-label="Upload Keyword JSON File"
          >
            <input
              type="file"
              id="keyword-file"
              accept=".json"
              hidden
              onChange={(e) =>
                handleFileChange('keyword', e.target.files?.[0] || null)
              }
            />
            <UploadFileIcon size="40" />
            <Typography variant="body1" mt={1}>
              Drag & Drop or Click to upload keyword config JSON
            </Typography>
            {keywordFile && (
              <Typography
                variant="body2"
                mt={1}
                color={fieldErrors.keywordFile ? 'error' : 'textPrimary'}
              >
                {keywordFile.name}
              </Typography>
            )}
          </DropZone>
        </FileUploadSection>
      ) : (
        <>
          {/* Supplier Config Table */}
          <SectionHeader>
            <Typography variant="h6">Supplier Configuration</Typography>
            <Button variant="outlined" size="small" onClick={addSupplierRow}>
              Add Row
            </Button>
          </SectionHeader>
          <ScrollableTableWrapper>
            <Table size="small">
              <TableHead>
                <TableRow>
                  {supplierColumns.map((col) => (
                    <StyledTableCell key={col}>
                      {col.charAt(0).toUpperCase() + col.slice(1)}
                    </StyledTableCell>
                  ))}
                  <StyledTableCell>Delete</StyledTableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {supplierRows.map((row, i) => (
                  <TableRow key={i}>
                    {supplierColumns.map((col) => (
                      <StyledTableCell key={col}>
                        <TextField
                          value={row[col] ?? ''}
                          onChange={(e) =>
                            updateSupplierCell(i, col, e.target.value)
                          }
                          variant="standard"
                          fullWidth
                          multiline
                          maxRows={3}
                          inputProps={{ style: { fontSize: 14 } }}
                        />
                      </StyledTableCell>
                    ))}
                    <StyledTableCell>
                      <IconButton
                        aria-label="delete supplier row"
                        size="small"
                        onClick={() => deleteSupplierRow(i)}
                      >
                        <DeleteIcon size="20" />
                      </IconButton>
                    </StyledTableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </ScrollableTableWrapper>

          {/* Keyword Config Table */}
          <SectionHeader>
            <Typography variant="h6">Keyword Configuration</Typography>
            <Button variant="outlined" size="small" onClick={addKeywordRow}>
              Add Row
            </Button>
          </SectionHeader>
          <ScrollableTableWrapper>
            <Table size="small">
              <TableHead>
                <TableRow>
                  {keywordColumns.map((col) => (
                    <StyledTableCell key={col}>
                      {col.charAt(0).toUpperCase() + col.slice(1)}
                    </StyledTableCell>
                  ))}
                  <StyledTableCell>Delete</StyledTableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {keywordRows.map((row, i) => (
                  <TableRow key={i}>
                    {keywordColumns.map((col) => (
                      <StyledTableCell key={col}>
                        <TextField
                          value={row[col] ?? ''}
                          onChange={(e) =>
                            updateKeywordCell(i, col, e.target.value)
                          }
                          variant="standard"
                          fullWidth
                          multiline
                          maxRows={3}
                          inputProps={{ style: { fontSize: 14 } }}
                        />
                      </StyledTableCell>
                    ))}
                    <StyledTableCell>
                      <IconButton
                        aria-label="delete keyword row"
                        size="small"
                        onClick={() => deleteKeywordRow(i)}
                      >
                        <DeleteIcon size="20" />
                      </IconButton>
                    </StyledTableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </ScrollableTableWrapper>
        </>
      )}

      {error && (
        <Typography variant="body2" color="error">
          {error}
        </Typography>
      )}

      <ButtonsRow>
        <Button
          variant="contained"
          color="primary"
          onClick={handleSubmit}
          disabled={isSubmitting}
          startIcon={isSubmitting ? <CircularProgress size={20} /> : null}
        >
          Submit
        </Button>
        <Button
          variant="contained"
          color="primary"
          onClick={handleReset}
          disabled={isSubmitting}
        >
          Reset
        </Button>
      </ButtonsRow>
    </Container>
  );
};

export default MarketRadar;
