import React, { useState } from 'react';
import Button from '@mui/material/Button';
import { TextField, Container, Box } from '@mui/material';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';

const AddUser = () => {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
  });

  const [role, setRole] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Handle form submission (e.g., send data to the server)
    console.log(formData);
  };

  const handleDropDownChange = (event: SelectChangeEvent) => {
    setRole(event.target.value as string);
  };

  return (
    <div className="add-user-wrapper">
      {/* <div className="right-content flex-col">
        <Button variant="contained" className="add-user-btn">
          Add user externally
        </Button>
      </div> */}
      <div>
        <Container>
          <Box sx={{ maxWidth: 400, margin: 'auto' }}>
            <div className="text-center">
              <h2>Add a new user</h2>
            </div>
            <form onSubmit={handleSubmit}>
              <TextField
                placeholder="First Name"
                variant="outlined"
                fullWidth
                margin="normal"
                name="firstName"
                value={formData.firstName}
                onChange={handleChange}
                required
              />
              <TextField
                placeholder="Last Name"
                variant="outlined"
                fullWidth
                margin="normal"
                name="lastName"
                value={formData.lastName}
                onChange={handleChange}
                required
              />
              <TextField
                placeholder="Email"
                variant="outlined"
                fullWidth
                margin="normal"
                name="email"
                value={formData.email}
                onChange={handleChange}
                type="email"
                required
              />
              <Button
                type="submit"
                variant="contained"
                color="primary"
                fullWidth
              >
                Submit
              </Button>
            </form>
          </Box>
        </Container>
      </div>
      <div className="hr-div"></div>
      <div className="assign-roles-wrapper">
        <div className="text-center">
          <h2>Assign roles</h2>
        </div>
        <div className="assign-roles-heading-wrapper">
          <h3>Tenants</h3>
          <h3>Roles</h3>
        </div>
        <div className="assign-roles-dropdown-wrapper">
          <span>Default Tenant</span>
          <Select
            labelId="demo-simple-select-label"
            id="demo-simple-select"
            value={role}
            label="Role"
            onChange={handleDropDownChange}
            className="role-dropdown"
          >
            <MenuItem value={'SAI-Admin'}>SAI-Admin</MenuItem>
            <MenuItem value={'SAI-CM'}>SAI-CM</MenuItem>
            <MenuItem value={'SAI-CPO'}>SAI-CPO</MenuItem>
            <MenuItem value={'SAI-CSP'}>SAI-CSP</MenuItem>
          </Select>
        </div>
        <div className="flex-end">
          <Button variant="contained" color="primary">
            Save Role
          </Button>
        </div>
      </div>
    </div>
  );
};

export default AddUser;
