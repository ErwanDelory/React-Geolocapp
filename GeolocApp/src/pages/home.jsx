import React, { useState } from 'react';
import { Button, Col, Container, Form, Row, Table } from 'react-bootstrap';
import { Map, TileLayer, Marker } from 'react-leaflet';
import { Icon } from 'leaflet';
import 'leaflet/dist/leaflet.css';

export const icon = new Icon({
  iconUrl: 'https://s3-us-west-2.amazonaws.com/s.cdpn.io/134893/pin-red.svg',
  iconSize: [25, 25],
});

const LocationMarker = ({ coord }) => {
  const coor = coord.split(',');
  return <Marker position={[coor[0], coor[1]]} icon={icon} />;
};

const Home = () => {
  const [latitude, setLatitude] = useState('46.227638');
  const [longitude, setLongitude] = useState('2.213749');
  const [name, setName] = useState('');
  const [message, setMessage] = useState('');
  const [lieu, setLieu] = useState([]);
  const [hierarchy, setHierarchy] = useState([]);

  const handleInputLatitudeChange = (event) => {
    const { value } = event.target;
    setLatitude(value);
  };

  const handleInputLongitudeChange = (event) => {
    const { value } = event.target;
    setLongitude(value);
  };

  const handleInputNameChange = (event) => {
    const { value } = event.target;
    setName(value);
  };

  const searchByCoord = () => {
    fetch('http://localhost:5000/api/find', {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ lat: latitude, lon: longitude, code: 4 }),
    })
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
        if (data.msg) {
          setMessage(data.msg);
        } else {
          setLieu(data.lieu);
          setHierarchy([]);
          setHierarchy(data.hierarchy);
          setMessage('');
        }
      });
  };

  const searchByName = () => {
    fetch(`http://localhost:5000/api/find/${name}/4`, {
      method: 'GET',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.msg) {
          setMessage(data.msg);
        } else {
          setLieu(data.lieu);
          setHierarchy([]);
          setHierarchy(data.hierarchy);
          setMessage('');
        }
      });
  };

  return (
    <Container className="homePage">
      <Form>
        <Form.Group controlId="ville">
          <Form.Label>Recherche par ville</Form.Label>
          <Form.Control
            type="text"
            placeholder="Saisir le nom d'une ville"
            value={name}
            onChange={handleInputNameChange}
          />
        </Form.Group>

        <Button variant="warning" onClick={searchByName}>
          Envoyer
        </Button>
      </Form>

      <br />
      <Table striped bordered hover size="sm">
        <thead>
          <tr>
            <th></th>
            <th>Lieux</th>
            <th>Latitude</th>
            <th>Longitude</th>
            <th>Population</th>
          </tr>
        </thead>
        <tbody>
          {lieu.map((data) => (
            <tr key={data.lat}>
              <td></td>
              <td>{data.name}</td>
              <td>{data.lat}</td>
              <td>{data.lon}</td>
              <td>{data.pop}</td>
            </tr>
          ))}
        </tbody>
      </Table>
      <br />
      {hierarchy.length > 0 && (
        <div>
          <p>La hiérarchie de la recherche est:</p>
        </div>
      )}
      <div className="hierarchie">
        {hierarchy.map((data) => (
          <p key={data.lat}>
            {' -> '}
            {data.name}
          </p>
        ))}
      </div>

      <Form>
        <Form.Group controlId="coord">
          <Form.Label>Recherche par coordonnées</Form.Label>
          <Row>
            <Col>
              Latitude
              <Form.Control
                type="number"
                placeholder="Saisir la latitude"
                value={latitude}
                onChange={handleInputLatitudeChange}
              />
            </Col>
            <Col>
              Longitude
              <Form.Control
                type="number"
                placeholder="Saisir la longitude"
                value={longitude}
                onChange={handleInputLongitudeChange}
              />
            </Col>
          </Row>
        </Form.Group>

        <Button variant="warning" onClick={searchByCoord}>
          Envoyer
        </Button>
      </Form>
      <p className="alert">{message}</p>

      <br />
      <Map center={[latitude, longitude]} zoom={6} scrollWheelZoom={false}>
        <TileLayer
          attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {lieu.map((data) => (
          <LocationMarker key={data.lat} coord={`${data.lat},${data.lon}`} />
        ))}
      </Map>
    </Container>
  );
};
export default Home;
