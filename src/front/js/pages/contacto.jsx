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
            <div className ="container">

                <h2><strong>Preguntas frecuentes</strong></h2>
                <br></br>
                <div className="accordion accordion-flush bg-dark text-white" id="accordionFlushExample">
                    {/* end */}
                    <div className="accordion-item">
                        <h2 className="accordion-header">
                            <button
                                className="accordion-button collapsed bg-dark text-white"
                                type="button"
                                data-bs-toggle="collapse"
                                data-bs-target="#flush-collapseOne"
                                aria-expanded="false"
                                aria-controls="flush-collapseOne">
                                <h4>¿Qué productos venden en la tienda?</h4>
                            </button>
                        </h2>
                        <div id="flush-collapseOne" className="accordion-collapse collapse" data-bs-parent="#accordionFlushExample">
                            <div className="accordion-body bg-dark text-white">
                            <p>Vendemos consolas, videojuegos nuevos y usados, accesorios 
                            y otros productos relacionados. También ofrecemos la posibilidad de que los usuarios vendan sus productos usados.</p>
                            </div>
                        </div>
                    </div>
                    {/* end */}
                    <div className="accordion-item">
                        <h2 className="accordion-header">
                            <button
                                className="accordion-button collapsed bg-dark text-white"
                                type="button"
                                data-bs-toggle="collapse"
                                data-bs-target="#flush-collapseTwo"
                                aria-expanded="false"
                                aria-controls="flush-collapseTwo">
                                <h4>¿Realizan envíos internacionales?</h4>
                            </button>
                        </h2>
                        <div id="flush-collapseTwo" className="accordion-collapse collapse" data-bs-parent="#accordionFlushExample">
                            <div className="accordion-body bg-dark text-white">
                            <p>No, actualmente no realizamos envíos internacionales. Solo ofrecemos envíos dentro de nuestra área de cobertura nacional.</p>
                            </div>
                        </div>
                    </div>
                    <div className="accordion-item">
                        <h2 className="accordion-header">
                            <button
                                className="accordion-button collapsed bg-dark text-white"
                                type="button"
                                data-bs-toggle="collapse"
                                data-bs-target="#flush-collapseThree"
                                aria-expanded="false"
                                aria-controls="flush-collapseThree">
                                <h4>¿Puedo devolver un producto si no estoy satisfecho?</h4>
                            </button>
                        </h2>
                        <div id="flush-collapseThree" className="accordion-collapse collapse" data-bs-parent="#accordionFlushExample">
                            <div className="accordion-body bg-dark text-white">
                            <p>Sí, aceptamos devoluciones dentro de los 14 días posteriores a la entrega, siempre que el producto esté en su empaque original y sin daños.</p>
                            </div>
                        </div>
                    </div>

                    <div className="accordion-item">
                        <h2 className="accordion-header">
                            <button
                                className="accordion-button collapsed bg-dark text-white"
                                type="button"
                                data-bs-toggle="collapse"
                                data-bs-target="#flush-collapseFour"
                                aria-expanded="false"
                                aria-controls="flush-collapseFour">
                                <h4>¿Puedo devolver un producto si no estoy satisfecho?</h4>
                            </button>
                        </h2>
                        <div id="flush-collapseFour" className="accordion-collapse collapse" data-bs-parent="#accordionFlushExample">
                            <div className="accordion-body bg-dark text-white">
                            <p>Sí, aceptamos devoluciones dentro de los 14 días posteriores a la entrega, siempre que el producto esté en su empaque original y sin daños.</p>
                            </div>
                        </div>
                    </div>

                    <div className="accordion-item">
                        <h2 className="accordion-header">
                            <button
                                className="accordion-button collapsed bg-dark text-white"
                                type="button"
                                data-bs-toggle="collapse"
                                data-bs-target="#flush-collapseFive"
                                aria-expanded="false"
                                aria-controls="flush-collapseFive">
                                <h4>¿Ofrecen garantía para las consolas?</h4>
                            </button>
                        </h2>
                        <div id="flush-collapseFive" className="accordion-collapse collapse" data-bs-parent="#accordionFlushExample">
                            <div className="accordion-body bg-dark text-white">
                            <p>Sí, todos nuestros productos tienen garantía del fabricante, que varía según la marca. Consulta los detalles específicos en la página del producto.</p>
                            </div>
                        </div>
                    </div>

                    <div className="accordion-item">
                        <h2 className="accordion-header">
                            <button
                                className="accordion-button collapsed bg-dark text-white"
                                type="button"
                                data-bs-toggle="collapse"
                                data-bs-target="#flush-collapseSix"
                                aria-expanded="false"
                                aria-controls="flush-collapseSix">
                                <h4>¿Qué métodos de pago aceptan?</h4>
                            </button>
                        </h2>
                        <div id="flush-collapseSix" className="accordion-collapse collapse" data-bs-parent="#accordionFlushExample">
                            <div className="accordion-body bg-dark text-white">
                            <p>Aceptamos tarjetas de crédito y débito, PayPal, y transferencias bancarias.</p>
                            </div>
                        </div>
                    </div>

                    <div className="accordion-item">
                        <h2 className="accordion-header">
                            <button
                                className="accordion-button collapsed bg-dark text-white"
                                type="button"
                                data-bs-toggle="collapse"
                                data-bs-target="#flush-collapseSeven"
                                aria-expanded="false"
                                aria-controls="flush-collapseSeven">
                                <h4>¿Puedo vender mis productos usados?</h4>
                            </button>
                        </h2>
                        <div id="flush-collapseSeven" className="accordion-collapse collapse" data-bs-parent="#accordionFlushExample">
                            <div className="accordion-body bg-dark text-white">
                            <p>Sí, puedes vender tus productos usados creando una cuenta y completando el formulario con fotos, descripción y precio.</p>
                            </div>
                        </div>
                    </div>

                    <div className="accordion-item">
                        <h2 className="accordion-header">
                            <button
                                className="accordion-button collapsed bg-dark text-white"
                                type="button"
                                data-bs-toggle="collapse"
                                data-bs-target="#flush-collapseEight"
                                aria-expanded="false"
                                aria-controls="flush-collapseEight">
                                <h4>¿Qué ventajas tiene la suscripción?</h4>
                            </button>
                        </h2>
                        <div id="flush-collapseEight" className="accordion-collapse collapse" data-bs-parent="#accordionFlushExample">
                            <div className="accordion-body bg-dark text-white">
                            <p>La suscripción ofrece una experiencia mejorada, acceso prioritario a ofertas especiales, 
                            envio gratis y soporte al cliente prioritario.</p>
                            </div>
                        </div>
                    </div>

                

                    <div className="accordion-item">
                        <h2 className="accordion-header">
                            <button
                                className="accordion-button collapsed bg-dark text-white"
                                type="button"
                                data-bs-toggle="collapse"
                                data-bs-target="#flush-collapseTen"
                                aria-expanded="false"
                                aria-controls="flush-collapseTen">
                                <h4>¿Cuánto tiempo tarda el envío?</h4>
                            </button>
                        </h2>
                        <div id="flush-collapseTen" className="accordion-collapse collapse" data-bs-parent="#accordionFlushExample">
                            <div className="accordion-body bg-dark text-white">
                            <p>El tiempo de envío varía según tu ubicación. Generalmente, los envíos nacionales tardan entre 2 y 7 días hábiles.
                                Te proporcionaremos un número de seguimiento para que puedas rastrear tu pedido.</p>
                            </div>
                        </div>
                    </div>

                    <div className="accordion-item">
                        <h2 className="accordion-header">
                            <button
                                className="accordion-button collapsed bg-dark text-white"
                                type="button"
                                data-bs-toggle="collapse"
                                data-bs-target="#flush-collapseEleven"
                                aria-expanded="false"
                                aria-controls="flush-collapseEleven">
                                <h4>¿Qué hago si el producto recibido está defectuoso o dañado?</h4>
                            </button>
                        </h2>
                        <div id="flush-collapseEleven" className="accordion-collapse collapse" data-bs-parent="#accordionFlushExample">
                            <div className="accordion-body bg-dark text-white">
                            <p>Si recibiste un producto defectuoso o dañado, por favor, contacta con nuestro equipo de atención al cliente inmediatamente. Te ayudaremos a procesar un reemplazo o reembolso.</p>
                            </div>
                        </div>
                    </div>

                    <div className="accordion-item">
                        <h2 className="accordion-header">
                            <button
                                className="accordion-button collapsed bg-dark text-white"
                                type="button"
                                data-bs-toggle="collapse"
                                data-bs-target="#flush-collapseTwelve"
                                aria-expanded="false"
                                aria-controls="flush-collapseTwelve">
                                <h4>¿Puedo cambiar la dirección de envío después de hacer el pedido?</h4>
                            </button>
                        </h2>
                        <div id="flush-collapseTwelve" className="accordion-collapse collapse" data-bs-parent="#accordionFlushExample">
                            <div className="accordion-body bg-dark text-white">
                            <p>Si necesitas cambiar la dirección de envío, por favor, contacta con nosotros lo antes posible. Si el pedido aún no ha sido procesado o enviado, podremos ayudarte a modificarla.</p>
                            </div>
                        </div>
                    </div>

                    <div className="accordion-item">
                        <h2 className="accordion-header">
                            <button
                                className="accordion-button collapsed bg-dark text-white"
                                type="button"
                                data-bs-toggle="collapse"
                                data-bs-target="#flush-collapseThirteen"
                                aria-expanded="false"
                                aria-controls="flush-collapseThirteen">
                                <h4>¿Qué consolas y accesorios ofrecen?</h4>
                            </button>
                        </h2>
                        <div id="flush-collapseThirteen" className="accordion-collapse collapse" data-bs-parent="#accordionFlushExample">
                            <div className="accordion-body bg-dark text-white">
                            <p>Contamos con una amplia variedad de consolas, juegos y accesorios para PlayStation, Xbox, Nintendo Switch, y PC. Si estás buscando algún modelo específico, no dudes en preguntarnos.</p>
                            </div>
                        </div>
                    </div>

                    <div className="accordion-item">
                        <h2 className="accordion-header">
                            <button
                                className="accordion-button collapsed bg-dark text-white"
                                type="button"
                                data-bs-toggle="collapse"
                                data-bs-target="#flush-collapseFourteen"
                                aria-expanded="false"
                                aria-controls="flush-collapseFourteen">
                                <h4>¿Cómo sé si un juego es compatible con mi consola?</h4>
                            </button>
                        </h2>
                        <div id="flush-collapseFourteen" className="accordion-collapse collapse" data-bs-parent="#accordionFlushExample">
                            <div className="accordion-body bg-dark text-white">
                            <p>En cada página de producto, indicamos claramente la plataforma para la que es compatible el juego. Si tienes alguna duda sobre la compatibilidad, puedes consultar con nuestro servicio de atención al cliente.</p>
                            </div>
                        </div>
                    </div>

                    <div className="accordion-item">
                        <h2 className="accordion-header">
                            <button
                                className="accordion-button collapsed bg-dark text-white"
                                type="button"
                                data-bs-toggle="collapse"
                                data-bs-target="#flush-collapseFifteen"
                                aria-expanded="false"
                                aria-controls="flush-collapseFifteen">
                                <h4>Tienen una tienda física donde pueda ver los productos?</h4>
                            </button>
                        </h2>
                        <div id="flush-collapseFifteen" className="accordion-collapse collapse" data-bs-parent="#accordionFlushExample">
                            <div className="accordion-body bg-dark text-white">
                            <p>Actualmente, operamos únicamente en línea. Sin embargo, puedes ver imágenes detalladas de cada producto y leer las especificaciones en nuestra tienda en línea.</p>
                            </div>
                        </div>
                    </div>

                    <div className="accordion-item">
                        <h2 className="accordion-header">
                            <button
                                className="accordion-button collapsed bg-dark text-white"
                                type="button"
                                data-bs-toggle="collapse"
                                data-bs-target="#flush-collapseSixteen"
                                aria-expanded="false"
                                aria-controls="flush-collapseSixteen">
                                <h4>¿Puedo comprar productos en tu tienda y enviarlos a una dirección diferente a la de facturación?</h4>
                            </button>
                        </h2>
                        <div id="flush-collapseSixteen" className="accordion-collapse collapse" data-bs-parent="#accordionFlushExample">
                            <div className="accordion-body bg-dark text-white">
                            <p>Sí, puedes enviar tus productos a una dirección diferente a la de facturación. Solo asegúrate de ingresar correctamente ambas direcciones durante el proceso de compra.</p>
                            </div>
                        </div>
                    </div>

                    <div className="accordion-item">
                        <h2 className="accordion-header">
                            <button
                                className="accordion-button collapsed bg-dark text-white"
                                type="button"
                                data-bs-toggle="collapse"
                                data-bs-target="#flush-collapseSeventeen"
                                aria-expanded="false"
                                aria-controls="flush-collapseSeventeen">
                                <h4>¿Los videojuegos tienen restricciones de región?</h4>
                            </button>
                        </h2>
                        <div id="flush-collapseSeventeen" className="accordion-collapse collapse" data-bs-parent="#accordionFlushExample">
                            <div className="accordion-body bg-dark text-white">
                            <p>Algunos videojuegos pueden tener restricciones de región. Asegúrate de verificar la compatibilidad de la región del producto antes de realizar la compra.</p>
                            </div>
                        </div>
                    </div>
                </div>
                <div clasName="faq">
                    <div className="container">
                        <p className="mt-5">
                            Para solicitar ayuda con un pedido escriba a <br />
                            <a href="mailto:finalbosshelp@finalboss.com" style={{ color: "#00aaff" }}>
                                finalbosshelp@finalboss.com
                            </a>
                        </p>
                
                        <div className="premium-container" style={{ display: 'flex', alignItems: 'center' }}>
    <Link className="premium-button" to="/suscripcion" style={{ marginRight: '10px' }}>
    Hazte Premium
    </Link>
    <img
        src="https://res.cloudinary.com/dr0wlij0c/image/upload/v1736455865/web-illustrations/r5r3z9kfuqd95yennokv.png"
        alt="Imagen FinalBoss Dudas"
        className="image"
        style={{ width: '10%', marginLeft: 'auto' }}
    />
</div>


<p>
    Contacto directo y mucho más...
</p>
                    
                    </div>
                    
                </div>
            </div>
        </>
    );
};
