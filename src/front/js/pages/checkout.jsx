import React, { useContext, useEffect, useState } from "react";
import { Context } from "../store/appContext";
import { Elements } from "@stripe/react-stripe-js";
import { loadStripe } from "@stripe/stripe-js";
import { CheckoutForm } from "../component/checkoutForm.jsx";
import "../../styles/checkout.css";

export const Checkout = () => {
  const stripePromise = loadStripe(process.env.STRIPE_PUBLISHABLE_KEY);
  const { store, actions } = useContext(Context);
  const [selectedSubscription, setSelectedSubscription] = useState(null);

  const calculateTotalPrice = () => {
    const cartTotal = store.shoppingCart?.reduce(
      (total, product) => total + (parseFloat(product.price) || 0),
      0
    ) || 0;

    const subscriptionPrice = selectedSubscription ? 9.99 : 0;
    const shippingPrice = (store.user?.subscription || isSubscriptionOnly) ? 0: 7;
    return cartTotal + subscriptionPrice + shippingPrice;
  };

  useEffect(() => {
    //prueba to see if subscr. was selected
    const hasSubscription = store.selectedSubscriptions?.includes("premium");
    setSelectedSubscription(hasSubscription ? "premium" : null);
  }, [store.selectedSubscriptions]);

  useEffect(() => {
    if (store.user) {
      actions.userShoppingCart();
    }
  }, [store.user]);

  useEffect(() => {
    if (store.selectedSubscriptions?.includes("premium")) {
      setSelectedSubscription("premium")
    }
  },[]);

  const handleSubscriptionToggle = () => {
    if (selectedSubscription) {
      setSelectedSubscription(null);
      actions.toggleSubscription("premium");
    } else {
      setSelectedSubscription("premium");
      actions.toggleSubscription("premium");
    }
  };

  const isSubscriptionOnly = (store.shoppingCart?.length === 0) && 
  (selectedSubscription || store.selectedSubscriptions?.includes("premium"))

  return (
    <div className="container order-summary">

      <div className="user-info">
        <h2>Información del Usuario</h2>
        {store.user && (
          <div>
            <img
              src={store.user.avatar || '/default-avatar.png'}
              alt="User avatar"
            />
            <div>
              <p>{store.user.userName}</p>
              <p>{store.user.email}</p>
              <p>Estado: {store.user.subscription ? 'Premium' : 'Basico'}</p>
            </div>
          </div>
        )}
      </div>

      <div className="accordion-item">
        <h2 className="accordion-header">
          <button
            className="accordion-button collapsed bg-light text-dark"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#flush-collapseOne"
            aria-expanded="false"
            aria-controls="flush-collapseOne">
            <h4>Direccion de envio</h4>
          </button>
        </h2>
        <div id="flush-collapseOne" className="accordion-collapse collapse" data-bs-parent="#accordionFlushExample">
          <div className="accordion-body bg-light text-dark">

            {/* in bootstrap*/}
            <div className="shipping-address">
              <h2>Dirección de Envío</h2>
              {store.user && (
                <>
                  <p>{store.user.address || 'No address provided'}</p>
                  <p>
                    {[
                      store.user.city,
                      store.user.postalCode,
                    ].filter(Boolean).join(", ")}
                  </p>
                </>
              )}
            </div>
            {/*end of sending location part */}

          </div>
        </div>
      </div>



      <div className="product-list">
        <h2>Lista de mis compras</h2>
        {store.shoppingCart?.length > 0 ? (
          <ul>
            {store.shoppingCart.map((product, index) => (
              <li className="Card" key={index}>
                <p className="product-incart">
                  {product.name} - {parseFloat(product.price).toFixed(2)}€
                </p>
              </li>
            ))}
          </ul>
        ) : (
          <p className="sinproductos">No hay productos en el carrito.</p>
        )}

        {/* subscription part start */}
        {!store.user?.subscription && (
          <div className="subscription-option">
            <label>
              <input
                type="checkbox"
                checked={Boolean(selectedSubscription)}
                onChange={handleSubscriptionToggle}
              />
              <p><strong>

                Añadir Suscripción Premium (9.99€/mes)
              </strong>
              </p>
            </label>
          </div>
        )}

        {/* subscription part end */}

        {!isSubscriptionOnly && (
          store.user?.subscription ? (
            <p className="shipping-fee">
              <span className="text-decoration-line-through text-dark">Gastos de envio: 7.00€</span>
              <span className="text-success ms-2">Gratis por ser usuario Premium!</span>
            </p>
          ) : (
            <p className="shipping-price">Gastos de envio: 7:00€</p>
          )
        )}

        <h3 className="total">Total: {calculateTotalPrice().toFixed(2)}€</h3>
      </div>

      <div className="container mt-4">
        <h1>Por favor, introduzca los datos de su tarjeta</h1>
        <Elements stripe={stripePromise}>
          <CheckoutForm totalAmount={calculateTotalPrice()} />
        </Elements>
      </div>
    </div>
  );
};