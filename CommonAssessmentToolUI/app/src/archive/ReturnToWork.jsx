import React from "react";
import PropTypes from "prop-types";
import { Card, CardContent, Typography } from "@mui/material";

function ReturnToWork({ returnToWork }) {
  return (
    <Card sx={{ maxWidth: 600, mt: 2, mx: "auto" }}>
      <CardContent>
        <Typography variant="h5" component="div">
          Predict If Return To Work
        </Typography>
        <Typography
          variant="body1"
          component="div"
          sx={{ textAlign: "center" }}
        >
          {returnToWork}
        </Typography>
      </CardContent>
    </Card>
  );
}

ReturnToWork.propTypes = {
  returnToWork: PropTypes.oneOfType([PropTypes.string, PropTypes.number])
    .isRequired,
};

export default ReturnToWork;
