import { useState } from 'react';
import styled from 'styled-components';
import Accordion from '@mui/material/Accordion';
import AccordionDetails from '@mui/material/AccordionDetails';
import AccordionSummary from '@mui/material/AccordionSummary';
import Typography from '@mui/material/Typography';
import { RolePermissions, SaiRoles } from '@/utils/constants';
import Switch from '@mui/material/Switch';

const PageContainer = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
  flex-direction: column;
  gap: 20px;
  width: 80%;
  margin: auto;
`;

const RoleDetails = () => {
  const [_, setExpanded] = useState<string | false>(false);

  const handleChange =
    (panel: string) => (_: React.SyntheticEvent, isExpanded: boolean) => {
      setExpanded(isExpanded ? panel : false);
    };

  return (
    <PageContainer>
      {SaiRoles.map((role, index) => (
        <Accordion
          defaultExpanded
          key={index}
          onChange={handleChange('panel1')}
          className="w-full"
        >
          <AccordionSummary
            // expandIcon={<ExpandMoreIcon />}
            aria-controls="panel1bh-content"
            id="panel1bh-header"
            className="user-mangement-accordion"
          >
            <Typography component="span" sx={{ width: '33%', flexShrink: 0 }}>
              <h3>{role}</h3>
            </Typography>
          </AccordionSummary>
          <AccordionDetails className="user-mangement-accordion-details">
            {RolePermissions.map((permission) => (
              <div key={permission} className="permission-row">
                <Typography>{permission}</Typography>
                <Switch />
              </div>
            ))}
          </AccordionDetails>
        </Accordion>
      ))}
    </PageContainer>
  );
};

export default RoleDetails;
