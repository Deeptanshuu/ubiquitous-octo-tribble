const express = require("express");
const cors = require("cors");
const { spawn } = require("child_process"); // Import child_process
const path = require("path");

const PORT = 8000;
const app = express();

app.use(cors({ origin: "*" }));

// Parse URL-encoded bodies and JSON bodies
app.use(express.urlencoded({ extended: false }));
app.use(express.json());

// Serve static files from the React app build folder or server folder
app.use(express.static(path.join(__dirname, "./dist/")));

// Start the Flask server
function startFlaskServer() {
  const flaskProcess = spawn("python", [
    path.join(__dirname, "./api/7k-tf-vectors.py"), // Adjusted to the correct path
  ]);

  flaskProcess.stdout.on("data", (data) => {
    console.log(`Flask: ${data}`);
  });

  flaskProcess.stderr.on("data", (data) => {
    console.error(`Flask Error: ${data}`);
  });

  flaskProcess.on("close", (code) => {
    console.log(`Flask server exited with code ${code}`);
  });

  return flaskProcess;
}

// Call the function to start Flask when starting Express
const flaskProcess = startFlaskServer();

// Catch all other routes and send back the React index file
app.get("/*", function (req, res) {
  res.sendFile(path.join(__dirname, "./dist/", "index.html"), function (err) {
    if (err) {
      res.status(500).send(err);
    }
  });
});

// Start the Express server
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});

// Shut down the Flask server when Node.js process exits
process.on("exit", () => {
  flaskProcess.kill();
});
