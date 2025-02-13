import React, { useContext, useEffect} from "react";
import { Context } from "../store/appContext";
import { Link } from "react-router-dom";
import "../../styles/contacto.css";

export const Contacto = () => {
    const { store, actions } = useContext(Context);
    useEffect(() => {
            window.scrollTo(0, 0); 
        }, []);

    return (
        <>
            <div className ="contact-container">
        <div className="divider"></div>
                <h2><strong>Preguntas frecuentes</strong></h2>
                <br></br>
                <div className="accordion accordion-flush my-accordion" id="accordionFlushExample">
                    {/* end */}
                    <div className="accordion-item">
                        <h2 className="accordion-header">
                            <button
                                className="accordion-button collapsed my-accordion"
                                type="button"
                                data-bs-toggle="collapse"
                                data-bs-target="#flush-collapseOne"
                                aria-expanded="false"
                                aria-controls="flush-collapseOne">
                                <h4 className="header-faq">¿Qué productos venden en la tienda?</h4>
                            </button>
                        </h2>
                        <div id="flush-collapseOne" className="accordion-collapse collapse" data-bs-parent="#accordionFlushExample">
                            <div className="accordion-body my-accordion">
                            <p className="contact-container-p">Vendemos consolas, videojuegos nuevos y usados, accesorios 
                            y otros productos relacionados. También ofrecemos la posibilidad de que los usuarios vendan sus productos usados.</p>
                            </div>
                        </div>
                    </div>
                    {/* end */}
                    <div className="accordion-item">
                        <h2 className="accordion-header">
                            <button
                                className="accordion-button collapsed my-accordion"
                                type="button"
                                data-bs-toggle="collapse"
                                data-bs-target="#flush-collapseTwo"
                                aria-expanded="false"
                                aria-controls="flush-collapseTwo">
                                <h4 className="header-faq">¿Realizan envíos internacionales?</h4>
                            </button>
                        </h2>
                        <div id="flush-collapseTwo" className="accordion-collapse collapse" data-bs-parent="#accordionFlushExample">
                            <div className="accordion-body my-accordion">
                            <p className="contact-container-p">No, actualmente no realizamos envíos internacionales. Solo ofrecemos envíos dentro de nuestra área de cobertura nacional.</p>
                            </div>
                        </div>
                    </div>

                    <div className="accordion-item">
                        <h2 className="accordion-header">
                            <button
                                className="accordion-button collapsed my-accordion"
                                type="button"
                                data-bs-toggle="collapse"
                                data-bs-target="#flush-collapseFour"
                                aria-expanded="false"
                                aria-controls="flush-collapseFour">
                                <h4 className="header-faq">¿Puedo devolver un producto si no estoy satisfecho?</h4>
                            </button>
                        </h2>
                        <div id="flush-collapseFour" className="accordion-collapse collapse" data-bs-parent="#accordionFlushExample">
                            <div className="accordion-body my-accordion">
                            <p className="contact-container-p">Sí, aceptamos devoluciones dentro de los 14 días posteriores a la entrega, siempre que el producto esté en su empaque original y sin daños.</p>
                            </div>
                        </div>
                    </div>

                    <div className="accordion-item">
                        <h2 className="accordion-header">
                            <button
                                className="accordion-button collapsed my-accordion"
                                type="button"
                                data-bs-toggle="collapse"
                                data-bs-target="#flush-collapseFive"
                                aria-expanded="false"
                                aria-controls="flush-collapseFive">
                                <h4 className="header-faq">¿Ofrecen garantía para las consolas?</h4>
                            </button>
                        </h2>
                        <div id="flush-collapseFive" className="accordion-collapse collapse" data-bs-parent="#accordionFlushExample">
                            <div className="accordion-body my-accordion">
                            <p className="contact-container-p">Sí, todos nuestros productos tienen garantía del fabricante, que varía según la marca. Consulta los detalles específicos en la página del producto.</p>
                            </div>
                        </div>
                    </div>

                    <div className="accordion-item">
                        <h2 className="accordion-header">
                            <button
                                className="accordion-button collapsed my-accordion"
                                type="button"
                                data-bs-toggle="collapse"
                                data-bs-target="#flush-collapseSix"
                                aria-expanded="false"
                                aria-controls="flush-collapseSix">
                                <h4 className="header-faq">¿Qué métodos de pago aceptan?</h4>
                            </button>
                        </h2>
                        <div id="flush-collapseSix" className="accordion-collapse collapse" data-bs-parent="#accordionFlushExample">
                            <div className="accordion-body my-accordion">
                            <p className="contact-container-p">Aceptamos tarjetas de crédito y débito, PayPal, y transferencias bancarias.</p>
                            </div>
                        </div>
                    </div>

                    <div className="accordion-item">
                        <h2 className="accordion-header">
                            <button
                                className="accordion-button collapsed my-accordion"
                                type="button"
                                data-bs-toggle="collapse"
                                data-bs-target="#flush-collapseSeven"
                                aria-expanded="false"
                                aria-controls="flush-collapseSeven">
                                <h4 className="header-faq">¿Puedo vender mis productos usados?</h4>
                            </button>
                        </h2>
                        <div id="flush-collapseSeven" className="accordion-collapse collapse" data-bs-parent="#accordionFlushExample">
                            <div className="accordion-body my-accordion">
                            <p className="contact-container-p">Sí, puedes vender tus productos usados creando una cuenta y completando el formulario con fotos, descripción y precio.</p>
                            </div>
                        </div>
                    </div>

                    <div className="accordion-item">
                        <h2 className="accordion-header">
                            <button
                                className="accordion-button collapsed my-accordion"
                                type="button"
                                data-bs-toggle="collapse"
                                data-bs-target="#flush-collapseEight"
                                aria-expanded="false"
                                aria-controls="flush-collapseEight">
                                <h4 className="header-faq">¿Qué ventajas tiene la suscripción?</h4>
                            </button>
                        </h2>
                        <div id="flush-collapseEight" className="accordion-collapse collapse" data-bs-parent="#accordionFlushExample">
                            <div className="accordion-body my-accordion">
                            <p className="contact-container-p">La suscripción ofrece una experiencia mejorada, acceso prioritario a ofertas especiales, 
                            envio gratis y soporte al cliente prioritario.</p>
                            </div>
                        </div>
                    </div>

                

                    <div className="accordion-item">
                        <h2 className="accordion-header">
                            <button
                                className="accordion-button collapsed my-accordion"
                                type="button"
                                data-bs-toggle="collapse"
                                data-bs-target="#flush-collapseTen"
                                aria-expanded="false"
                                aria-controls="flush-collapseTen">
                                <h4 className="header-faq">¿Cuánto tiempo tarda el envío?</h4>
                            </button>
                        </h2>
                        <div id="flush-collapseTen" className="accordion-collapse collapse" data-bs-parent="#accordionFlushExample">
                            <div className="accordion-body my-accordion">
                            <p className="contact-container-p">El tiempo de envío varía según tu ubicación. Generalmente, los envíos nacionales tardan entre 2 y 7 días hábiles.
                                Te proporcionaremos un número de seguimiento para que puedas rastrear tu pedido.</p>
                            </div>
                        </div>
                    </div>

                    <div className="accordion-item">
                        <h2 className="accordion-header">
                            <button
                                className="accordion-button collapsed my-accordion"
                                type="button"
                                data-bs-toggle="collapse"
                                data-bs-target="#flush-collapseEleven"
                                aria-expanded="false"
                                aria-controls="flush-collapseEleven">
                                <h4 className="header-faq">¿Qué hago si el producto recibido está defectuoso o dañado?</h4>
                            </button>
                        </h2>
                        <div id="flush-collapseEleven" className="accordion-collapse collapse" data-bs-parent="#accordionFlushExample">
                            <div className="accordion-body my-accordion">
                            <p className="contact-container-p">Si recibiste un producto defectuoso o dañado, por favor, contacta con nuestro equipo de atención al cliente inmediatamente. Te ayudaremos a procesar un reemplazo o reembolso.</p>
                            </div>
                        </div>
                    </div>

                    <div className="accordion-item">
                        <h2 className="accordion-header">
                            <button
                                className="accordion-button collapsed my-accordion"
                                type="button"
                                data-bs-toggle="collapse"
                                data-bs-target="#flush-collapseTwelve"
                                aria-expanded="false"
                                aria-controls="flush-collapseTwelve">
                                <h4 className="header-faq">¿Puedo cambiar la dirección de envío después de hacer el pedido?</h4>
                            </button>
                        </h2>
                        <div id="flush-collapseTwelve" className="accordion-collapse collapse" data-bs-parent="#accordionFlushExample">
                            <div className="accordion-body my-accordion">
                            <p className="contact-container-p">Si necesitas cambiar la dirección de envío, por favor, contacta con nosotros lo antes posible. Si el pedido aún no ha sido procesado o enviado, podremos ayudarte a modificarla.</p>
                            </div>
                        </div>
                    </div>

                    <div className="accordion-item">
                        <h2 className="accordion-header">
                            <button
                                className="accordion-button collapsed my-accordion"
                                type="button"
                                data-bs-toggle="collapse"
                                data-bs-target="#flush-collapseThirteen"
                                aria-expanded="false"
                                aria-controls="flush-collapseThirteen">
                                <h4 className="header-faq">¿Qué consolas y accesorios ofrecen?</h4>
                            </button>
                        </h2>
                        <div id="flush-collapseThirteen" className="accordion-collapse collapse" data-bs-parent="#accordionFlushExample">
                            <div className="accordion-body my-accordion">
                            <p className="contact-container-p">Contamos con una amplia variedad de consolas, juegos y accesorios para PlayStation, Xbox, Nintendo Switch, y PC. Si estás buscando algún modelo específico, no dudes en preguntarnos.</p>
                            </div>
                        </div>
                    </div>

                    <div className="accordion-item">
                        <h2 className="accordion-header">
                            <button
                                className="accordion-button collapsed my-accordion"
                                type="button"
                                data-bs-toggle="collapse"
                                data-bs-target="#flush-collapseFourteen"
                                aria-expanded="false"
                                aria-controls="flush-collapseFourteen">
                                <h4 className="header-faq">¿Cómo sé si un juego es compatible con mi consola?</h4>
                            </button>
                        </h2>
                        <div id="flush-collapseFourteen" className="accordion-collapse collapse" data-bs-parent="#accordionFlushExample">
                            <div className="accordion-body my-accordion">
                            <p className="contact-container-p">En cada página de producto, indicamos claramente la plataforma para la que es compatible el juego. Si tienes alguna duda sobre la compatibilidad, puedes consultar con nuestro servicio de atención al cliente.</p>
                            </div>
                        </div>
                    </div>

                    <div className="accordion-item">
                        <h2 className="accordion-header">
                            <button
                                className="accordion-button collapsed my-accordion"
                                type="button"
                                data-bs-toggle="collapse"
                                data-bs-target="#flush-collapseFifteen"
                                aria-expanded="false"
                                aria-controls="flush-collapseFifteen">
                                <h4 className="header-faq">Tienen una tienda física donde pueda ver los productos?</h4>
                            </button>
                        </h2>
                        <div id="flush-collapseFifteen" className="accordion-collapse collapse" data-bs-parent="#accordionFlushExample">
                            <div className="accordion-body my-accordion">
                            <p className="contact-container-p">Actualmente, operamos únicamente en línea. Sin embargo, puedes ver imágenes detalladas de cada producto y leer las especificaciones en nuestra tienda en línea.</p>
                            </div>
                        </div>
                    </div>

                    <div className="accordion-item">
                        <h2 className="accordion-header">
                            <button
                                className="accordion-button collapsed my-accordion"
                                type="button"
                                data-bs-toggle="collapse"
                                data-bs-target="#flush-collapseSixteen"
                                aria-expanded="false"
                                aria-controls="flush-collapseSixteen">
                                <h4 className="header-faq">¿Puedo comprar productos en tu tienda y enviarlos a una dirección diferente a la de facturación?</h4>
                            </button>
                        </h2>
                        <div id="flush-collapseSixteen" className="accordion-collapse collapse" data-bs-parent="#accordionFlushExample">
                            <div className="accordion-body my-accordion">
                            <p className="contact-container-p">Sí, puedes enviar tus productos a una dirección diferente a la de facturación. Solo asegúrate de ingresar correctamente ambas direcciones durante el proceso de compra.</p>
                            </div>
                        </div>
                    </div>

                    <div className="accordion-item">
                        <h2 className="accordion-header">
                            <button
                                className="accordion-button collapsed my-accordion"
                                type="button"
                                data-bs-toggle="collapse"
                                data-bs-target="#flush-collapseSeventeen"
                                aria-expanded="false"
                                aria-controls="flush-collapseSeventeen">
                                <h4 className="header-faq">¿Los videojuegos tienen restricciones de región?</h4>
                            </button>
                        </h2>
                        <div id="flush-collapseSeventeen" className="accordion-collapse collapse" data-bs-parent="#accordionFlushExample">
                            <div className="accordion-body my-accordion">
                            <p className="contact-container-p">Algunos videojuegos pueden tener restricciones de región. Asegúrate de verificar la compatibilidad de la región del producto antes de realizar la compra.</p>
                            </div>
                        </div>
                    </div>
                </div>
               <div className="divider"></div>
                     <section className="row faq-home">
                       <div className="col-12 col-lg-9">
                         <p className="faq-home-p">Para solicitar ayuda con un pedido escriba a <Link to="/contacto" className="faq-home-p-a">help@finalboss.com</Link></p>
                         <Link to="/suscripcion" className="faq-home-button">Hazte premium</Link>
                         <p className="faq-home-p">Contacto directo y mucho más...</p>
                       </div>
                       <figure className=" col-8 col-lg-3 text-start ms-5 ms-lg-0">
                         <img src="https://res.cloudinary.com/dshjlidcs/image/upload/v1738526760/r5r3z9kfuqd95yennokv-min_mcza4i.png" alt="FAQ" className="img-fluid" />
                       </figure>
                     </section>
                     <div className="divider"></div>
            </div>
        </>
    );
};
