import React from 'react';
import { Navbar } from 'react-bootstrap';

const NavbarApp = ({ title }) => {
  return (
    <Navbar bg="light" className="justify-content-center">
      <Navbar.Brand>{title}</Navbar.Brand>
    </Navbar>
  );
};
export default NavbarApp;
