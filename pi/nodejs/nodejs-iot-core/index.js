const express = require("express");
const socketIo = require("socket.io");
const http = require("http");
const bodyParser = require("body-parser");
const DB = require("./models/index");
const PORT = process.env.PORT || 81;
const app = express();
const cors = require("cors");
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());
app.use(
  cors({
    origin: "*",
  })
);
var tmp = 0;

const server = require("http").createServer(app);
const io = socketIo(server, {
  pingTimeout: 30000,
  upgrades: ["websocket", "polling"],
  cors: {
    origin: "*",
  },
});

let rev = 0;

app.get("/setalert", (req, res) => {
  hightmp = req.query.hightmp;
  lowtmp = req.query.lowtmp;
  DB.Alerts.update({ highTMP: hightmp, lowTMP: lowtmp }, { where: { id: 1 } })
    .then((result) => {
      res.json({ success: "yes", data: result });
    })
    .catch((err) => {
      res.json({ success: "no" });
    });
});
app.get("/getalert", (req, res) => {
  DB.Alerts.findOne({ where: { id: 1 } })
    .then((data) => {
      res.json({
        success: "yes",
        data: {
          highTMP: data.highTMP,
          lowTMP: data.lowTMP,
        },
      });
    })
    .catch((err) => {
      res.json({ success: "no", data: err });
    });
});
app.get("/setdata", (req, res) => {
  tmp = req.query.tmp;
  SensorName = req.query.name;
  console.log("TMP: ", tmp);
  io.to("browser").emit("tmp", tmp);
  DB.Alerts.findOne({ where: { id: 1 } })
    .then((data) => {
      io.to("browser").emit("alert", {
        data: {
          highTMP: data.highTMP,
          lowTMP: data.lowTMP,
          tmp: tmp,
        },
      });
    })
    .catch((err) => {});

  DB.Logs.create({ SensorName: SensorName, Value: tmp })
    .then(() => {
      res.json({ success: "yes" });
    })
    .catch((err) => {
      res.json({ success: "no" });
    });
});
app.get("/getdata", (req, res) => {
  row = req.query.row;
  row = parseInt(row);
  if (!(row >= 1)) {
    row = 50;
  }
  DB.Logs.findAll({ limit: row, order: [["createdAt", "DESC"]] }).then(
    (data) => {
      res.json({ success: "yes", data });
    }
  );
});

io.on("connection", (socket) => {
  console.log(
    "Socket Client connected: ",
    socket.handshake.query.device,
    " ID : ",
    socket.id,
    " & IP : ",
    socket.handshake.address,
    " Transport : ",
    socket.handshake.query.transport,
    " Version : ",
    socket.handshake.query.EIO,
    " Header : ",
    socket.header
  );
  if (socket.handshake.query.device == "browser") {
    socket.join("browser");
  }

  socket.on("disconnect", (reason) => {
    console.log(reason);
  });
});
server.listen(PORT, (err) => {
  if (err) console.log(err);
  console.log("Server running on Port ", PORT);
});
