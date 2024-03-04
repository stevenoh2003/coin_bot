import React, { useEffect, useState } from "react";
import { Line, Bar } from "react-chartjs-2";
import axios from "axios";
import { Chart, registerables } from "chart.js";
import "chartjs-adapter-date-fns";

// Make sure to import a CSS file that includes the font and additional styles
import "./App.css"; // Assuming you create this

Chart.register(...registerables);

function WebApp() {
  const server_url = "http://172.20.10.4:5001/";
  const baseURL = server_url;

  const [timeSeriesData, setTimeSeriesData] = useState([]);
  const [distributionData, setDistributionData] = useState({});
  const [currentTotalCoins, setCurrentTotalCoins] = useState(0);

    const [withdrawAmount, setWithdrawAmount] = useState("");
    const [message, setMessage] = useState(null); // To store success or error messages

    const withdrawCoins = async () => {
      try {
        // Update the parameter to 'amount' to match the updated backend endpoint
        const response = await axios.get(`${server_url}withdraw_coin`, {
          params: { amount: withdrawAmount }, // Changed from 'value' to 'amount'
        });
        // Update the success message to include detailed withdrawal information if provided by the backend
        const successMessage = response.data.details
          ? `Withdrawn successfully. Details: ${response.data.details["100_yen_coins"]} x 100 yen coins and ${response.data.details["10_yen_coins"]} x 10 yen coins.`
          : response.data.message;
        setMessage({ type: "success", text: successMessage });
        // You might want to update your coins data here if necessary
        // For example, if you have a state managing the counts of coins, you should update it accordingly
      } catch (error) {
        if (error.response && error.response.data && error.response.data.error) {
          setMessage({ type: "error", text: error.response.data.error });
        } else {
          setMessage({
            type: "error",
            text: "An error occurred while withdrawing coins.",
          });
        }
      }
    };


  const distributionChartOptions = {
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          stepSize: 1,
          precision: 0,
        },
        title: {
          display: true,
          text: "Number of Coins",
        },
      },
    },
    plugins: {
      legend: {
        display: true,
      },
    },
  };

      const add10Yen = () => {
        axios
          .post(`${baseURL}add_10_yen`)
          .then((response) => {
            alert("10 yen added successfully");
            console.log(response.data);
          })
          .catch((error) => console.error("There was an error!", error));
      };

      const add100Yen = () => {
        axios
          .post(`${baseURL}add_100_yen`)
          .then((response) => {
            alert("100 yen added successfully");
            console.log(response.data);
          })
          .catch((error) => console.error("There was an error!", error));
      };

      const subtract10Yen = () => {
        axios
          .post(`${baseURL}subtract_10_yen`)
          .then((response) => {
            alert("10 yen subtracted successfully");
            console.log(response.data);
          })
          .catch((error) => console.error("There was an error!", error));
      };

      const subtract100Yen = () => {
        axios
          .post(`${baseURL}subtract_100_yen`)
          .then((response) => {
            alert("100 yen subtracted successfully");
            console.log(response.data);
          })
          .catch((error) => console.error("There was an error!", error));
      };

  useEffect(() => {
    const fetchTimeSeriesData = async () => {
      const response = await axios.get(server_url + "total_over_time");
      setTimeSeriesData(response.data); // Assuming this is an array of { timestamp, totalAmount }
    };

    const fetchDistributionData = async () => {
      const response = await axios.get(server_url + "total");
      setDistributionData({
        labels: ["10 Yen", "100 Yen"],
        datasets: [
          {
            label: "Number of Coins",
            data: [
              response.data.coins["10_yen"].count,
              response.data.coins["100_yen"].count,
            ],
            backgroundColor: [
              "rgba(255, 99, 132, 0.2)",
              "rgba(54, 162, 235, 0.2)",
            ],
          },
        ],
      });
    };



    const fetchCurrentTotalCoins = async () => {
      const response = await axios.get(server_url + "total");
      if (response.data && response.data.total_amount !== undefined) {
        setCurrentTotalCoins(response.data.total_amount);
      }
    };

    fetchTimeSeriesData();
    fetchDistributionData();
    fetchCurrentTotalCoins();

    // Set up polling every 10 seconds (10000 milliseconds)
    const interval = setInterval(() => {
      fetchTimeSeriesData();
      fetchDistributionData();
      fetchCurrentTotalCoins();
    }, 1000);

    // Clean up interval on component unmount
    return () => clearInterval(interval);
  }, []);

  const timeSeriesChartData = {
    labels: timeSeriesData.map((data) =>
      new Date(data.timestamp).toLocaleDateString()
    ),
    datasets: [
      {
        label: "Total Coins Over Time",
        data: timeSeriesData.map((data) => data.totalAmount),
        fill: false,
        borderColor: "rgb(75, 192, 192)",
        tension: 0.1,
      },
    ],
  };

  return (
    <div className="app-container">
      <div className="top-row">
        <div className="total-coins-display">
          合計金額：
          {currentTotalCoins}
        </div>
        <div className="gamepad-control">
          <div className="withdraw-section">
            <button className="gamepad-button" onClick={subtract10Yen}>
              Withdraw 10
            </button>
            <button className="gamepad-button" onClick={subtract100Yen}>
              Withdraw 100
            </button>
          </div>

          <div className="pickup-section">
            <button className="gamepad-button" onClick={add10Yen}>
              Pick 10
            </button>
            <button className="gamepad-button" onClick={add100Yen}>
              Pick 100
            </button>
          </div>

          {message && (
            <div className={`message ${message.type}`}>{message.text}</div>
          )}
        </div>
      </div>
      <div className="charts-row">
        <div className="chart-container">
          <h2>Total Coins Over Time</h2>
          {timeSeriesData.length > 0 && <Line data={timeSeriesChartData} />}
        </div>
        <div className="chart-container">
          <h2>Distribution of Coins</h2>
          {distributionData.labels && (
            <Bar data={distributionData} options={distributionChartOptions} />
          )}
        </div>
      </div>
    </div>
  );
}

export default WebApp;
