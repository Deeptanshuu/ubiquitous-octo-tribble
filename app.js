const express = require("express");
const cors = require("cors");
const PORT = 8181;
const app = express();

// Serve static files from the React app buil folder or server folder

const path = require('path');

app.use(express.static(path.join(__dirname, './dist/')));

app.get('/*', function(req, res) {
  res.sendFile(path.join(__dirname, './dist/', 'index.html'),
   function(err) {
    if (err) {
      res.status(500).send(err);
    }
  });

});

app.use(cors({ origin: '*' }));

// Parse URL-encoded bodies
app.use(express.urlencoded({ extended: false }));
app.use(express.json()); // Parse JSON bodies

app.listen(PORT, () => {
    console.log(`Server is running on port http://localhost:${PORT}`);
  });