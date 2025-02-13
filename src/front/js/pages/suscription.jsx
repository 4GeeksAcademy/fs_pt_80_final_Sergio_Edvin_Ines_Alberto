import React, { useContext } from "react";
import { Context } from "../store/appContext";
import { Link, useNavigate } from "react-router-dom";
import "../../styles/suscripcion.css";

export const Suscription = () => {
    const { store, actions } = useContext(Context);
    const navigate = useNavigate();

    const handleSubscriptionClick = (e) => {
        e.preventDefault();

        const subscriptionId = "premium";
        actions.toggleSubscription(subscriptionId);

        navigate("/checkout");
    };


    return (
        <>
        <div className="body-suscription">
                <h2><strong>Conviértete en Premium Boss</strong></h2>
                <h3 className="h3-suscription">Únete a nuestra comunidad y disfruta de las mejores ventajas.</h3>
            <div className="card-container row">

                <div className="card basic ">
                    <div className="circle-icon">
                        <img
                            src="https://res.cloudinary.com/dshjlidcs/image/upload/v1738526759/j8e22hpsiepivnue4rby-min_dbfghd.png"
                            alt="Basic subscription user illustration"
                        />
                    </div>
                    <ul className="text text-start px-3">
                        <li><i class="fa-regular icon-suscription fa-circle"></i> Descuentos estándares</li>
                        <li><i class="fa-regular icon-suscription fa-circle"></i> Tarifas de envío regulares</li>
                        <li><i class="fa-regular icon-suscription fa-circle"></i> Visibilidad limitada de tus productos</li>
                        <li><i class="fa-regular icon-suscription fa-circle"></i> Acceso a contenido general</li>
                        <li><i class="fa-regular icon-suscription fa-circle"></i> Soporte y asistencia estándar</li>
                    </ul>
                 
                </div>

                <div className="card premium">
                    
                    <div className="circle-icon">
                        <img
                            src="https://res.cloudinary.com/dshjlidcs/image/upload/v1738526760/t9wliafde7eongd3umez-min_usjcnx.png"
                            alt="Premium subscription user illustration"
                        />
                    </div>
                    <img className="premium-img"
                    src="https://res.cloudinary.com/dshjlidcs/image/upload/v1738527220/web-img/n0mqeqtviwcpjyhqkyen.png"
                    alt="premium boss"/>
                    <ul className="text text-start px-lg-3">
                        <li><i class="fa-regular icon-suscription-2 fa-star"></i> Descuentos exclusivos</li>
                        <li><i class="fa-regular icon-suscription-2 fa-star"></i> Envíos gratuitos</li>
                        <li><i class="fa-regular icon-suscription-2 fa-star"></i> Mejora de la visibilidad de tus productos</li>
                        <li><i class="fa-regular icon-suscription-2 fa-star"></i> Acceso anticipado a contenido exclusivo</li>
                        <li><i class="fa-regular icon-suscription-2 fa-star"></i> Soporte mejorado incluyendo servicio 24 horas al día, 7 días a la semana</li>
                    </ul>
                    <div className="container">
                    <p><strong className="price">9.99€</strong><span>/mes</span></p>
                    <Link
                     className="faq-home-button" 
                     to="/checkout"
                     onClick={handleSubscriptionClick}
                    >
                        <strong>¡Únete!</strong>
                    </Link>

                    </div>
                </div>
            </div>
            </div>
        </>
    );
};
