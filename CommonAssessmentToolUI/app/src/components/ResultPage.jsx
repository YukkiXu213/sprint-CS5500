import React from "react";
import { useLocation, useNavigate, Link } from "react-router-dom";
import {
  Card,
  CardActions,
  CardContent,
  Typography,
  Button,
  Paper,
  Grid,
  Box,
  CircularProgress,
} from "@mui/material";
import { handleSaveReport } from "./ReportGenerate";

const ResultPage = () => {
  const location = useLocation();
  const navigate = useNavigate();

  const { id, selectedUser, probability, interventions } = location.state || {
    id: null,
    selectedUser: {},
    probability: 0,
    interventions: [],
  };

  const handleSaveReportClick = (format) => {
    handleSaveReport(format, selectedUser, probability, interventions);
  };

  const handleBackToForm = () => {
    if (id !== undefined && id !== null) {
      navigate(`/client/${id}`);
    } else {
      navigate("/form", { state: { selectedUser } });
    }
  };

  const formatIntervention = (intervention) => {
    if (Array.isArray(intervention) && intervention.length === 2) {
      const percentage = intervention[0];
      const types = intervention[1];
      if (Array.isArray(types)) {
        return {
          types: types.join(", "),
          percentage: `${percentage.toFixed(1)}%`,
        };
      }
    }
    return { types: "Invalid data", percentage: "" };
  };

  return (
    <Box sx={{ p: 4, maxWidth: 1000, margin: "0 auto" }}>
      <Paper elevation={3} sx={{ p: 4 }}>
        <Typography
          variant="h3"
          gutterBottom
          sx={{
            mb: 4,
            fontFamily: "'Open Sans', sans-serif",
            fontWeight: 500,
            color: "#2c3e50",
          }}
        >
          Assessment Result
        </Typography>

        {/* Probability with Progress Bar */}
        <Box align="center" sx={{ mb: 5 }}>
          <Box
            align="center"
            sx={{ position: "relative", display: "inline-flex", mb: 2 }}
          >
            {/* Circular Progress */}
            <CircularProgress
              variant="determinate"
              value={probability}
              size="8rem"
              sx={{
                color: "primary.main",
              }}
            />
            {/* Probability inside the circle */}
            <Box
              sx={{
                position: "absolute",
                top: "50%",
                left: "50%",
                transform: "translate(-50%, -50%)",
              }}
            >
              <Typography
                variant="h4"
                color="primary"
                sx={{ fontWeight: "bold" }}
              >
                {probability.toFixed(1)}%
              </Typography>
            </Box>
          </Box>
          <Typography
            variant="h5"
            sx={{ fontWeight: "bold" }}
            color="primary"
            gutterBottom
          >
            Return-to-Work Probability
          </Typography>
        </Box>

        {/* Recommended Interventions */}
        <Box sx={{ mb: 4, p: 3 }}>
          <Typography variant="h5" sx={{ mb: 2, color: "#2c3e50" }}>
            Recommended Interventions
          </Typography>
          <Grid container spacing={3}>
            {interventions.map((intervention, index) => {
              const formatted = formatIntervention(intervention);
              const interventionKey = formatted.types
                .replace(/[\s,]/g, "-")
                .toLowerCase();

              return (
                <Grid item xs={12} sm={6} md={4} key={index}>
                  <Card
                    variant="outlined"
                    sx={{
                      boxShadow: 2,
                      "&:hover": {
                        transform: "scale(1.05)",
                        transition: "transform 0.2s ease",
                      },
                    }}
                  >
                    <CardContent>
                      <Typography
                        variant="h6"
                        sx={{ color: "#2c3e50", fontWeight: "bold", mb: 1 }}
                      >
                        {formatted.types}
                      </Typography>
                      <Typography
                        variant="h6"
                        component="span"
                        sx={{ fontWeight: "bold", color: "primary.main" }}
                      >
                        + {formatted.percentage}
                      </Typography>
                    </CardContent>
                    <CardActions>
                      <Button
                        component={Link}
                        to={`/interventions/${interventionKey}`}
                        size="small"
                        color="primary"
                      >
                        View Details
                      </Button>
                    </CardActions>
                  </Card>
                </Grid>
              );
            })}
          </Grid>
        </Box>

        {/* Action Buttons */}
        <Box sx={{ display: "flex", justifyContent: "flex-end", mt: 4 }}>
          <Grid container spacing={3} sx={{ width: 550, mt: 4 }}>
            <Grid item xs={12} sm={4}>
              <Button
                variant="contained"
                color="primary"
                onClick={() => handleSaveReportClick("pdf")}
                fullWidth
              >
                Save as PDF
              </Button>
            </Grid>
            <Grid item xs={12} sm={4}>
              <Button
                variant="contained"
                color="secondary"
                onClick={() => handleSaveReportClick("csv")}
                fullWidth
              >
                Save as CSV
              </Button>
            </Grid>
            <Grid item xs={12} sm={4}>
              <Button variant="outlined" onClick={handleBackToForm} fullWidth>
                Back to Form
              </Button>
            </Grid>
          </Grid>
        </Box>
      </Paper>
    </Box>
  );
};

export default ResultPage;
