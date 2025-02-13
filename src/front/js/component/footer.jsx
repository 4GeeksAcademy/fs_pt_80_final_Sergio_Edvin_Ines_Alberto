import React, { Component } from "react";
import "../../styles/footer.css"
import { Link } from "react-router-dom";

export const Footer = () => (
	<footer className="footer mt-1 p-3 my-footer">
		<div className="container d-flex align-items-stretch ">
		<div className=" col-8 col-md-4 mt-md-5 mt-3 me-0 p-0">
			<p className="copyrigth"><b>© FinalBoss</b> 2025</p>
		</div>	
		<div className="text-center col-4 ms-3">
			<img src="https://res.cloudinary.com/dshjlidcs/image/upload/v1738526761/tneodtjquec1aboexsmw-min_bfkxfx.png" className="img-fluid" alt="" />
		</div>
		<div className="col-4 text-end footer-menu mt-2 me-0 p-0 d-flex flex-column">	
			
			<Link to="/perfil">Perfil</Link>
			<Link to="/store">Catálogo</Link>
			<Link to="/contacto">FaQ</Link>
		
		</div>
		</div>	
	</footer>
);
