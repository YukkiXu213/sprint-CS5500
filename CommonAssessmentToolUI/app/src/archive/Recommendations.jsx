// Recommendations.js
import React from "react";
import PropTypes from "prop-types";
import {
  Card,
  CardContent,
  Typography,
  List,
  ListItem,
  ListItemText,
  Divider,
} from "@mui/material";

function Recommendations({ recommendations }) {
  return (
    <Card sx={{ maxWidth: 600, mt: 2, mx: "auto" }}>
      <CardContent>
        <Typography variant="h5" component="div">
          Recommended Interventions
        </Typography>
        <List>
          {Array.isArray(recommendations) &&
            recommendations.map((item, index) => (
              <React.Fragment key={index}>
                <ListItem>
                  <ListItemText primary={item} />
                </ListItem>
                <Divider component="li" />
              </React.Fragment>
            ))}
        </List>
      </CardContent>
    </Card>
  );
}

// Add PropTypes validation
Recommendations.propTypes = {
  recommendations: PropTypes.arrayOf(PropTypes.string).isRequired, // Validate as an array of strings
};

// Add Default Props
Recommendations.defaultProps = {
  recommendations: [], // Default to an empty array
};

export default Recommendations;
