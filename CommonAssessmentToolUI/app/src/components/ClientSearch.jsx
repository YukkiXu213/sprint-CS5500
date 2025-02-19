import React, { useState, useEffect } from "react";
import axios from "axios";
import { useLocation, useNavigate } from "react-router-dom";
import "./ClientSearch.css";
import { Avatar, Card, Typography, Box } from "@mui/material";

function useQuery() {
  return new URLSearchParams(useLocation().search);
}

function ClientSearch() {
  const [clients, setClients] = useState([]);
  const [error, setError] = useState(null);
  const navigate = useNavigate();
  const query = useQuery().get("query");

  const defaultValues = {
    work_experience: 0,
    canada_workex: 0,
    dep_num: 0,
    canada_born: "false",
    citizen_status: "",
    level_of_schooling: "",
    fluent_english: "false",
    reading_english_scale: 0,
    speaking_english_scale: 0,
    writing_english_scale: 0,
    numeracy_scale: 0,
    computer_scale: 0,
    transportation_bool: "false",
    caregiver_bool: "false",
    housing: "",
    income_source: "",
    felony_bool: "false",
    attending_school: "false",
    currently_employed: "false",
    substance_use: "false",
    time_unemployed: 0,
    need_mental_health_support_bool: "false",
  };

  const fieldLabels = {
    firstName: "First Name",
    lastName: "Last Name",
    age: "Age",
    gender: "Gender",
    work_experience: "Work Experience",
    canada_workex: "Canada Work Experience",
    dep_num: "Number of Dependents",
    canada_born: "Born in Canada",
    citizen_status: "Citizen Status",
    level_of_schooling: "Level of Schooling",
    fluent_english: "Fluent in English",
    reading_english_scale: "Reading English Scale",
    speaking_english_scale: "Speaking English Scale",
    writing_english_scale: "Writing English Scale",
    numeracy_scale: "Numeracy Scale",
    computer_scale: "Computer Scale",
    transportation_bool: "Has Transportation",
    caregiver_bool: "Is a Caregiver",
    housing: "Housing",
    income_source: "Source of Income",
    felony_bool: "Has Felony",
    attending_school: "Attending School",
    currently_employed: "Currently Employed",
    substance_use: "Substance Use",
    time_unemployed: "Time Unemployed",
    need_mental_health_support_bool: "Needs Mental Health Support",
  };

  useEffect(() => {
    if (query) {
      handleSearch(query);
    }
  }, [query]);

  const handleSearch = async (query) => {
    try {
      const params = { firstName: query };
      const response = await axios.get(
        `http://localhost:3001/api/clients/search`,
        {
          params: params,
        },
      );
      setClients(response.data);
      setError(null);
    } catch (err) {
      setError("Error fetching clients. Please try again.");
      console.error("Fetch error:", err);
    }
  };

  const handleClientClick = (clientId) => {
    navigate(`/client/${clientId}`);
  };

  return (
    <div>
      <link
        rel="stylesheet"
        href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css"
      />
      <Typography
        variant="h4"
        align="center"
        gutterBottom
        sx={{ marginTop: "40px" }}
      >
        Search Results for First Name &quot;{query}&quot;
      </Typography>

      {error && <div className="error-message">{error}</div>}

      <div className="client-grid">
        {clients.length > 0 ? (
          clients.map((client) => {
            const nonDefaultFields = Object.keys(defaultValues)
              .filter(
                (field) =>
                  client[field] !== undefined &&
                  client[field] !== defaultValues[field],
              )
              .slice(0, 4);

            return (
              <Card
                key={client.id}
                className="client-card"
                onClick={() => handleClientClick(client.id)}
              >
                <Box display="flex" alignItems="center" mb={1}>
                  <Avatar className="client-avatar" />
                  <Box ml={2}>
                    <Typography variant="h6" component="div" fontWeight="bold">
                      {client.firstName} {client.lastName}
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      {client.age} years, {client.gender}
                    </Typography>
                  </Box>
                </Box>
                <Box mt={2}>
                  {nonDefaultFields.slice(0, 4).map((field) => (
                    <Typography key={field} variant="body2">
                      <span className="field-label">{fieldLabels[field]}:</span>
                      <span className="field-value">
                        {client[field].toString()}
                      </span>
                    </Typography>
                  ))}
                </Box>
                <Box display="flex" justifyContent="flex-end" mt={1}>
                  <Typography
                    variant="caption"
                    sx={{
                      fontSize: "0.75rem",
                      fontStyle: "italic",
                      color: "#999",
                    }}
                  >
                    Last Update:{" "}
                    {client.last_update
                      ? new Date(client.last_update).toLocaleString()
                      : "No updates yet"}
                  </Typography>
                </Box>
              </Card>
            );
          })
        ) : (
          <div>No clients found for your search.</div>
        )}
      </div>
    </div>
  );
}

export default ClientSearch;
