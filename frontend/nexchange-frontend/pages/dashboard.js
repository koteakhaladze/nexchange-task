import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Line} from 'react-chartjs-2';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
  } from 'chart.js'

  ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
  )
const Dashboard = () => {
  const [completionTimes, setCompletionTimes] = useState(0);
  const [quote, setQuote] = useState('');
  const [base, setBase] = useState('');
  const [pair, setPair] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [currencies, setCurrencies] = useState([]);
  const [pairs, setPairs] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchData();
    fetchCurrencies();
  }, []);

  const fetchCurrencies = async () => {
    const response = await axios.get(
        'http://localhost:8000/api/orders/pairs',
        {withCredentials: false}
    );
    setCurrencies(response.data.currencies.map((currency) => currency.name));
    setPairs(response.data.pairs.map((pair) => pair.name));
  };

  const fetchData = async () => {
    const searchParams = new URLSearchParams();
    if (pair !== '') {
        searchParams.append("pair", pair);
    }
    if (quote !== '') {
        searchParams.append("quote", quote);
    }
    if (base !== '') {
        searchParams.append("base", base);
    }
    if (startDate !== '') {
        searchParams.append("date_from", startDate);
    }
    if (endDate !== '') {
        searchParams.append("date_to", endDate);
    }
    try {
    const response = await axios.get(
      'http://localhost:8000/api/orders/processing-time',
      {params: searchParams},
      {withCredentials: false}
    );
        setCompletionTimes(response.data.avg);
        setError('');
    } catch (error) {
        setError(error.response.data.non_field_errors[0]);
    }
  };

  const handleQuoteChange = (e) => {
    setQuote(e.target.value);
  };

  const handlePairChange = (e) => {
    setPair(e.target.value);
  };

  const handleBaseChange = (e) => {
    setBase(e.target.value);
  };

  const handleStartDateChange = (e) => {
    setStartDate(e.target.value);
  };

  const handleEndDateChange = (e) => {
    setEndDate(e.target.value);
  };

  const chartData = {
    labels: ["time"],
    datasets: [
      {
        label: 'Average Completion Time',
        data: [completionTimes],
        fill: false,
        borderColor: 'rgba(75,192,192,1)',
      },
    ],
  };

  return (
    <div>
      <h1>Dashboard</h1>
      {error && <p style={{ color: 'red'}}>{error}</p>}
      <div>
        <label>Pair:</label>
        <select type="text" value={pair} onChange={handlePairChange}>
            <option value="">None</option>
            {pairs.map((pair) => <option value={pair}>{pair}</option>)}
        </select>
      </div>
      <div>
        <label>Quote:</label>
        <select type="text" value={quote} onChange={handleQuoteChange}>
            <option value="">None</option>
            {currencies.map((currency) => <option value={currency}>{currency}</option>)}
        </select>
      </div>
      <div>
        <label>Base:</label>
        <select type="text" value={base} onChange={handleBaseChange}>
             <option value="">None</option>
            {currencies.map((currency) => <option value={currency}>{currency}</option>)}
        </select>
      </div>
      <div>
        <label>Start Date:</label>
        <input type="date" value={startDate} onChange={handleStartDateChange} />
      </div>
      <div>
        <label>End Date:</label>
        <input type="date" value={endDate} onChange={handleEndDateChange} />
      </div>
      <div>
        <button onClick={fetchData}>Fetch Data</button>
      </div>
      <div>
        <Line data={chartData} />
      </div>
    </div>
  );
};

export default Dashboard;
