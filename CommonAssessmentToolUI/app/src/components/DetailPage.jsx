import React, { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import {
  Grid,
  Card,
  Typography,
  Box,
  IconButton,
  Button,
  FormControl,
  Select,
  MenuItem,
} from "@mui/material";
import axios from "axios";
import styles from "./Form.detail.css";

function Client() {
  const navigate = useNavigate();
  const { id } = useParams();

  // Map of field names to their labels
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
    last_update: "Last Update",
  };

  const [selectedUser, setSelectedUser] = useState({
    firstName: "",
    lastName: "",
    age: 0,
    gender: "",
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
    last_update: "", // Track last update timestamp
  });

  const [editMode, setEditMode] = useState({});

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const response = await axios.get(
          `http://localhost:3001/api/client/${id}`,
        );
        setSelectedUser(response.data);
      } catch (error) {
        console.error("Error fetching user data:", error);
      }
    };

    fetchUserData();
  }, [id]);

  const handleEditClick = (field) => {
    setEditMode((prev) => ({
      ...prev,
      [field]: true,
    }));
  };

  const handleConfirmClick = async (field) => {
    try {
      // Validation for required fields
      if (field === "firstName" || field === "lastName") {
        if (!selectedUser[field].trim()) {
          alert(`${fieldLabels[field]} cannot be empty.`);
          return;
        }
      }

      // Validation for age
      if (field === "age") {
        const age = selectedUser[field];
        if (age < 18 || age > 65) {
          alert("Age should be between 18 and 65.");
          return;
        }
      }

      // If validation passes, proceed with the update
      const currentTimestamp = new Date().toISOString(); // Get current time in ISO format
      const updatedData = {
        [field]: selectedUser[field],
        last_update: currentTimestamp, // Update last_update field
      };

      await axios.put(
        `http://localhost:3001/api/update-user/${id}`,
        updatedData,
      );

      setSelectedUser((prevUser) => ({
        ...prevUser,
        last_update: currentTimestamp, // Update state with the new timestamp
      }));

      setEditMode((prev) => ({
        ...prev,
        [field]: false,
      }));

      alert(
        `${fieldLabels[field]} updated successfully! Last update: ${new Date(currentTimestamp).toLocaleString()}`,
      );
    } catch (error) {
      console.error("Error updating user data:", error);
      alert("Failed to update user.");
    }
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setSelectedUser({
      ...selectedUser,
      [name]: type === "checkbox" ? (checked ? "true" : "false") : value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const unconfirmedFields = Object.keys(editMode).filter(
      (field) => editMode[field],
    );
    if (unconfirmedFields.length > 0) {
      const unconfirmedFieldLabels = unconfirmedFields.map(
        (field) => `"${fieldLabels[field]}" Field`,
      );
      alert(`${unconfirmedFieldLabels.join(", ")} edit not confirmed.`);
      return;
    }

    try {
      const response = await axios.post(
        "http://localhost:3001/api/work-score",
        selectedUser,
      );

      const probability = response.data.baseline;
      const interventions = response.data.interventions;

      navigate("/results", {
        state: { id, selectedUser, probability, interventions },
      });
    } catch (error) {
      console.error("Error submitting form:", error);
    }
  };

  const renderEditableField = (
    fieldName,
    label,
    type = "text",
    selectOptions = null,
  ) => (
    <Grid item xs={12} sm={6} key={fieldName}>
      <div className={`${styles.inputContainer} input-container`}>
        <div className={`${styles.labelContainer} label-container`}>
          <Typography
            variant="subtitle1"
            style={{ color: "#666", fontWeight: 500 }}
          >
            {label}
          </Typography>
          {!editMode[fieldName] && (
            <IconButton
              onClick={() => handleEditClick(fieldName)}
              size="small"
              className={styles.editIconButton}
            >
              <i className="fas fa-edit edit-icon" />
            </IconButton>
          )}
        </div>
        {!editMode[fieldName] ? (
          <Typography variant="body1">{selectedUser[fieldName]}</Typography>
        ) : (
          <Box
            className={styles.editFieldContainer}
            sx={{ display: "flex", alignItems: "center", gap: 1 }}
          >
            {type === "boolean" ? (
              <FormControl className={styles.booleanDropdown}>
                <Select
                  name={fieldName}
                  value={selectedUser[fieldName]}
                  onChange={handleChange}
                >
                  <MenuItem value="true">true</MenuItem>
                  <MenuItem value="false">false</MenuItem>
                </Select>
              </FormControl>
            ) : selectOptions ? (
              <FormControl fullWidth>
                <Select
                  name={fieldName}
                  value={selectedUser[fieldName]}
                  onChange={handleChange}
                >
                  {selectOptions.map((option) => (
                    <MenuItem key={option.value} value={option.value}>
                      {option.label}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            ) : (
              <input
                type={type}
                name={fieldName}
                value={selectedUser[fieldName]}
                onChange={handleChange}
                className={styles.editInputField}
              />
            )}
            <IconButton
              onClick={() => handleConfirmClick(fieldName)}
              size="small"
              className={styles.confirmIconButton}
            >
              <i className="fas fa-check confirm-icon" />
            </IconButton>
          </Box>
        )}
      </div>
    </Grid>
  );

  return (
    <Box sx={{ width: 800, margin: "50px auto" }}>
      <link
        rel="stylesheet"
        href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css"
      />
      <Card className={styles.card}>
        <Typography
          variant="h4"
          component="h2"
          gutterBottom
          className="form-title"
        >
          Client Detail
        </Typography>

        <Typography
          variant="subtitle2"
          color="textSecondary"
          sx={{
            mb: 2,
            textAlign: "right",
            marginRight: 3, // Add right margin
          }}
        >
          Last Update:{" "}
          {selectedUser.last_update
            ? new Date(selectedUser.last_update).toLocaleString()
            : "No updates yet"}
        </Typography>

        <div className={`${styles.sectionTitle} section-title`}>
          Personal Info
        </div>
        <Grid container spacing={3}>
          {renderEditableField("firstName", "First Name")}
          {renderEditableField("lastName", "Last Name")}
          {renderEditableField("age", "Age", "number")}
          {renderEditableField("gender", "Gender", "text", [
            { value: "", label: "None" },
            { value: "M", label: "Male" },
            { value: "F", label: "Female" },
          ])}
          {renderEditableField("dep_num", "Number of Dependents", "number")}
        </Grid>
        <div className={`${styles.sectionTitle} section-title`}>
          Work Experience
        </div>
        <Grid container spacing={4}>
          {renderEditableField("work_experience", "Work Experience", "number")}
          {renderEditableField(
            "canada_workex",
            "Canada Work Experience",
            "number",
          )}
          {renderEditableField(
            "currently_employed",
            "Currently Employed",
            "boolean",
          )}
          {renderEditableField(
            "time_unemployed",
            "Time Unemployed (months)",
            "number",
          )}
        </Grid>

        <div className={`${styles.sectionTitle} section-title`}>
          Citizenship
        </div>
        <Grid container spacing={4}>
          {renderEditableField("citizen_status", "Citizen Status", "text", [
            { value: "", label: "None" },
            { value: "citizen", label: "Citizen" },
            { value: "permanent_resident", label: "Permanent Resident" },
            { value: "temporary_resident", label: "Temporary Resident" },
          ])}
          {renderEditableField("canada_born", "Born in Canada", "boolean")}
        </Grid>

        <div className={`${styles.sectionTitle} section-title`}>Education</div>
        <Grid container spacing={4}>
          {renderEditableField(
            "attending_school",
            "Attending School",
            "boolean",
          )}
          {renderEditableField(
            "fluent_english",
            "Fluent in English",
            "boolean",
          )}
          {renderEditableField(
            "level_of_schooling",
            "Level of Schooling",
            "text",
            [
              { value: "Grade 0-8", label: "Grade 0-8" },
              { value: "Grade 9", label: "Grade 9" },
              { value: "Grade 10", label: "Grade 10" },
              { value: "Grade 11", label: "Grade 11" },
              {
                value: "Grade 12 or equivalent",
                label: "Grade 12 or equivalent",
              },
              { value: "Some college", label: "Some college" },
              { value: "Bachelor’s degree", label: "Bachelor’s degree" },
              { value: "Post graduate", label: "Post graduate" },
            ],
          )}
          {renderEditableField(
            "reading_english_scale",
            "Reading English Scale (0-10)",
            "number",
          )}
          {renderEditableField(
            "speaking_english_scale",
            "Speaking English Scale (0-10)",
            "number",
          )}
          {renderEditableField(
            "writing_english_scale",
            "Writing English Scale (0-10)",
            "number",
          )}
          {renderEditableField(
            "numeracy_scale",
            "Numeracy Scale (0-10)",
            "number",
          )}
          {renderEditableField(
            "computer_scale",
            "Computer Scale (0-10)",
            "number",
          )}
        </Grid>

        <div className={`${styles.sectionTitle} section-title`}>Other</div>
        <Grid container spacing={4} sx={{ paddingBottom: 3 }}>
          {renderEditableField("housing", "Housing", "text", [
            { value: "Renting-private", label: "Renting-private" },
            { value: "Renting-subsidized", label: "Renting-subsidized" },
            { value: "Homeowner", label: "Homeowner" },
            { value: "Institution", label: "Institution" },
          ])}
          {renderEditableField("income_source", "Source of Income", "text", [
            { value: "Employment", label: "Employment" },
            { value: "Self-Employment", label: "Self-Employment" },
            {
              value: "Ontario Works applied or receiving",
              label: "Ontario Works applied or receiving",
            },
          ])}
          {renderEditableField(
            "transportation_bool",
            "Has Transportation",
            "boolean",
          )}
          {renderEditableField("caregiver_bool", "Is a Caregiver", "boolean")}
          {renderEditableField("felony_bool", "Has Felony", "boolean")}
          {renderEditableField("substance_use", "Substance Use", "boolean")}
          {renderEditableField(
            "need_mental_health_support_bool",
            "Needs Mental Health Support",
            "boolean",
          )}
        </Grid>
      </Card>

      <Box sx={{ display: "flex", justifyContent: "flex-end", marginTop: 3 }}>
        <Button
          type="submit"
          variant="contained"
          color="secondary"
          onClick={handleSubmit}
          sx={{
            minWidth: "200px",
            height: "60px",
            fontSize: "1rem",
          }}
        >
          See your score
        </Button>
      </Box>
    </Box>
  );
}

export default Client;

// import React, { useState, useEffect } from 'react';
// import { useNavigate, useParams } from 'react-router-dom';
// import {
//   Grid,
//   Card,
//   Typography,
//   Box,
//   IconButton,
//   Button,
//   FormControl,
//   Select,
//   MenuItem,
//   Divider,
// } from "@mui/material";
// import axios from 'axios';
// import styles from "./Form.detail.css";

// function Client() {
//   const navigate = useNavigate();
//   const { id } = useParams();
//   const [open, setOpen] = useState(true);

//   // Map of field names to their labels
//   const fieldLabels = {
//     firstName: "First Name",
//     lastName: "Last Name",
//     age: "Age",
//     gender: "Gender",
//     work_experience: "Work Experience",
//     canada_workex: "Canada Work Experience",
//     dep_num: "Number of Dependents",
//     canada_born: "Born in Canada",
//     citizen_status: "Citizen Status",
//     level_of_schooling: "Level of Schooling",
//     fluent_english: "Fluent in English",
//     reading_english_scale: "Reading English Scale",
//     speaking_english_scale: "Speaking English Scale",
//     writing_english_scale: "Writing English Scale",
//     numeracy_scale: "Numeracy Scale",
//     computer_scale: "Computer Scale",
//     transportation_bool: "Has Transportation",
//     caregiver_bool: "Is a Caregiver",
//     housing: "Housing",
//     income_source: "Source of Income",
//     felony_bool: "Has Felony",
//     attending_school: "Attending School",
//     currently_employed: "Currently Employed",
//     substance_use: "Substance Use",
//     time_unemployed: "Time Unemployed",
//     need_mental_health_support_bool: "Needs Mental Health Support",
//   };

//   const [selectedUser, setSelectedUser] = useState({
//     firstName: "",
//     lastName: "",
//     age: 0,
//     gender: "",
//     work_experience: 0,
//     canada_workex: 0,
//     dep_num: 0,
//     canada_born: "false",
//     citizen_status: "",
//     level_of_schooling: "",
//     fluent_english: "false",
//     reading_english_scale: 0,
//     speaking_english_scale: 0,
//     writing_english_scale: 0,
//     numeracy_scale: 0,
//     computer_scale: 0,
//     transportation_bool: "false",
//     caregiver_bool: "false",
//     housing: "",
//     income_source: "",
//     felony_bool: "false",
//     attending_school: "false",
//     currently_employed: "false",
//     substance_use: "false",
//     time_unemployed: 0,
//     need_mental_health_support_bool: "false",
//   });

//   const [editMode, setEditMode] = useState({});

//   useEffect(() => {
//     const fetchUserData = async () => {
//       try {
//         const response = await axios.get(`http://localhost:3001/api/client/${id}`);
//         setSelectedUser(response.data);
//       } catch (error) {
//         console.error("Error fetching user data:", error);
//       }
//     };

//     fetchUserData();
//   }, [id]);

//   const handleEditClick = (field) => {
//     setEditMode((prev) => ({
//       ...prev,
//       [field]: true,
//     }));
//   };

//   const handleConfirmClick = async (field) => {
//     try {
//       const updatedData = { [field]: selectedUser[field] };
//       await axios.put(`http://localhost:3001/api/update-user/${id}`, updatedData);

//       setEditMode((prev) => ({
//         ...prev,
//         [field]: false,
//       }));
//       alert(`${fieldLabels[field]} updated successfully!`);
//     } catch (error) {
//       console.error("Error updating user data:", error);
//       alert('Failed to update user.');
//     }
//   };

//   const handleChange = (e) => {
//     const { name, value, type, checked } = e.target;
//     setSelectedUser({
//       ...selectedUser,
//       [name]: type === 'checkbox' ? (checked ? "true" : "false") : value,
//     });
//   };

//   const handleSubmit = async (e) => {
//     e.preventDefault();

//     // Check for unconfirmed fields
//     const unconfirmedFields = Object.keys(editMode).filter((field) => editMode[field]);
//     if (unconfirmedFields.length > 0) {
//       const unconfirmedFieldLabels = unconfirmedFields.map(field => `"${fieldLabels[field]}" Field`);
//       alert(`${unconfirmedFieldLabels.join(", ")} edit not confirmed.`);
//       return;
//     }

//     try {
//       const response = await axios.post('http://localhost:3001/api/work-score', selectedUser);

//       const probability = response.data.baseline;
//       const interventions = response.data.interventions;

//       console.log(selectedUser);
//       navigate("/results", { state: { id, selectedUser, probability, interventions } });
//     } catch (error) {
//       console.error("Error submitting form:", error);
//     }
//   };

//   const renderEditableField = (fieldName, label, type = "text", selectOptions = null) => (
//     <Grid item xs={12} sm={6} key={fieldName}>
//       <div className={`${styles.inputContainer} input-container`}>
//         <div className={`${styles.labelContainer} label-container`}>
//           <Typography variant="subtitle1" style={{ color: '#888', fontWeight: 500 }}>
//             {label}
//           </Typography>
//           {!editMode[fieldName] && (
//             <IconButton onClick={() => handleEditClick(fieldName)} size="small" className={styles.editIconButton}>
//               <i className="fas fa-edit edit-icon" />
//             </IconButton>
//           )}
//         </div>
//         {!editMode[fieldName] ? (
//           <Typography variant="body1">
//             {selectedUser[fieldName]}
//           </Typography>
//         ) : (
//           <Box className={styles.editFieldContainer} sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
//             {type === "boolean" ? (
//               <FormControl className={styles.booleanDropdown}>
//                 <Select
//                   name={fieldName}
//                   value={selectedUser[fieldName]}
//                   onChange={handleChange}
//                 >
//                   <MenuItem value="true">true</MenuItem>
//                   <MenuItem value="false">false</MenuItem>
//                 </Select>
//               </FormControl>
//             ) : selectOptions ? (
//               <FormControl fullWidth>
//                 <Select
//                   name={fieldName}
//                   value={selectedUser[fieldName]}
//                   onChange={handleChange}
//                 >
//                   {selectOptions.map((option) => (
//                     <MenuItem key={option.value} value={option.value}>
//                       {option.label}
//                     </MenuItem>
//                   ))}
//                 </Select>
//               </FormControl>
//             ) : (
//               <input
//                 type={type}
//                 name={fieldName}
//                 value={selectedUser[fieldName]}
//                 onChange={handleChange}
//                 className={styles.editInputField}
//               />
//             )}
//             <IconButton onClick={() => handleConfirmClick(fieldName)} size="small" className={styles.confirmIconButton}>
//               <i className="fas fa-check confirm-icon" />
//             </IconButton>
//           </Box>
//         )}
//       </div>
//     </Grid>
//   );

//   return (
//     <Box sx={{ width: 800, margin: '50px auto' }}>
//       <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" />
//       <Card className={styles.card}>
//         <Typography
//           variant="h4"
//           component="h2"
//           gutterBottom
//           className="form-title"
//         >
//           Client Detail
//         </Typography>

//         <div className={`${styles.sectionTitle} section-title`}>Personal Info</div>
//         <Grid container spacing={3}>
//           {renderEditableField("firstName", "First Name")}
//           {renderEditableField("lastName", "Last Name")}
//           {renderEditableField("age", "Age", "number")}
//           {renderEditableField("gender", "Gender", "text", [
//             { value: "", label: "None" },
//             { value: "M", label: "Male" },
//             { value: "F", label: "Female" },
//           ])}
//           {renderEditableField("dep_num", "Number of Dependents", "number")}
//         </Grid>
//         <div className={`${styles.sectionTitle} section-title`}>Work Experience</div>
//         <Grid container spacing={4}>
//           {renderEditableField("work_experience", "Work Experience", "number")}
//           {renderEditableField("canada_workex", "Canada Work Experience", "number")}
//           {renderEditableField("currently_employed", "Currently Employed", "boolean")}
//           {renderEditableField("time_unemployed", "Time Unemployed (months)", "number")}
//         </Grid>

//         <div className={`${styles.sectionTitle} section-title`}>Citizenship</div>
//         <Grid container spacing={4}>
//           {renderEditableField("citizen_status", "Citizen Status", "text", [
//             { value: "", label: "None" },
//             { value: "citizen", label: "Citizen" },
//             { value: "permanent_resident", label: "Permanent Resident" },
//             { value: "temporary_resident", label: "Temporary Resident" },
//           ])}
//           {renderEditableField("canada_born", "Born in Canada", "boolean")}
//         </Grid>

//         <div className={`${styles.sectionTitle} section-title`}>Education</div>
//         <Grid container spacing={4}>
//           {renderEditableField("attending_school", "Attending School", "boolean")}
//           {renderEditableField("fluent_english", "Fluent in English", "boolean")}
//           {renderEditableField("level_of_schooling", "Level of Schooling", "text", [
//             { value: "Grade 0-8", label: "Grade 0-8" },
//             { value: "Grade 9", label: "Grade 9" },
//             { value: "Grade 10", label: "Grade 10" },
//             { value: "Grade 11", label: "Grade 11" },
//             { value: "Grade 12 or equivalent", label: "Grade 12 or equivalent" },
//             { value: "Some college", label: "Some college" },
//             { value: "Bachelor’s degree", label: "Bachelor’s degree" },
//             { value: "Post graduate", label: "Post graduate" },
//           ])}
//           {renderEditableField("reading_english_scale", "Reading English Scale (0-10)", "number")}
//           {renderEditableField("speaking_english_scale", "Speaking English Scale (0-10)", "number")}
//           {renderEditableField("writing_english_scale", "Writing English Scale (0-10)", "number")}
//           {renderEditableField("numeracy_scale", "Numeracy Scale (0-10)", "number")}
//           {renderEditableField("computer_scale", "Computer Scale (0-10)", "number")}
//         </Grid>

//         <div className={`${styles.sectionTitle} section-title`} >Other</div>
//         <Grid container spacing={4} sx={{ paddingBottom: 3 }}>
//           {renderEditableField("housing", "Housing", "text", [
//             { value: "Renting-private", label: "Renting-private" },
//             { value: "Renting-subsidized", label: "Renting-subsidized" },
//             { value: "Homeowner", label: "Homeowner" },
//             { value: "Institution", label: "Institution" },
//           ])}
//           {renderEditableField("income_source", "Source of Income", "text", [
//             { value: "Employment", label: "Employment" },
//             { value: "Self-Employment", label: "Self-Employment" },
//             { value: "Ontario Works applied or receiving", label: "Ontario Works applied or receiving" },
//           ])}
//           {renderEditableField("transportation_bool", "Has Transportation", "boolean")}
//           {renderEditableField("caregiver_bool", "Is a Caregiver", "boolean")}
//           {renderEditableField("felony_bool", "Has Felony", "boolean")}
//           {renderEditableField("substance_use", "Substance Use", "boolean")}
//           {renderEditableField("need_mental_health_support_bool", "Needs Mental Health Support", "boolean")}
//         </Grid>

//       </Card>

//       <Box sx={{ display: 'flex', justifyContent: 'flex-end', marginTop: 3 }}>
//         <Button
//           type="submit"
//           variant="contained"
//           color="secondary"
//           onClick={handleSubmit}
//           sx={{
//             minWidth: '200px',
//             height: '60px',
//             fontSize: '1rem'
//           }}
//         >
//           See your score
//         </Button>
//       </Box>
//     </Box>
//   );
// }

// export default Client;
