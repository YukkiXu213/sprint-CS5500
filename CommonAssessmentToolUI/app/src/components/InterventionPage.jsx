import React from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Box, Typography, Paper, Button } from "@mui/material";

const InterventionPage = () => {
  const { interventionKey } = useParams(); // Extract the dynamic path parameter
  const navigate = useNavigate();

  // Revert "-" back to spaces and capitalize each word
  const interventionName = interventionKey
    .replace(/-/g, " ") // Replace "-" with spaces
    .replace(/\b\w/g, (char) => char.toUpperCase()); // Capitalize first letter of each word

  return (
    <Box sx={{ p: 4, maxWidth: 800, margin: "0 auto" }}>
      <Paper elevation={3} sx={{ p: 4 }}>
        <Typography
          variant="h3"
          gutterBottom
          align="center"
          sx={{
            fontFamily: "'Open Sans', sans-serif",
            fontWeight: 500,
            color: "#2c3e50",
          }}
        >
          {interventionName}
        </Typography>
        <Typography variant="body1" align="center">
          This is a dummy page for the {interventionName} intervention.
        </Typography>
        <Box textAlign="center" sx={{ mt: 4 }}>
          <Button
            variant="outlined"
            color="primary"
            onClick={() => navigate(-1)} // Navigate back to the previous page
          >
            Back to your result
          </Button>
        </Box>
      </Paper>
    </Box>
  );
};

export default InterventionPage;
