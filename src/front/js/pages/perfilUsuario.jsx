import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { useContext } from "react";
import { Context } from "../store/appContext";
import "../../styles/perfil.css";

import { ProductCard } from "../component/product-small-card.jsx";
import { Reviews } from "../component/reviews.jsx";

export const PerfilUsuario = () => {
    const { actions, store } = useContext(Context);
    const { userId } = useParams(); // Obtener el ID del usuario desde la URL
    const [userData, setUserData] = useState(null); // Estado local para los datos del usuario
    const [favoritesDetails, setFavoritesDetails] = useState([]);
    const [loading, setLoading] = useState(true); // Para controlar el estado de carga

    // Petición para obtener los datos del usuario
    useEffect(() => {
        const fetchUserProfile = async () => {
            try {
                const data = await actions.getUserProfile(userId); // Llama a la acción para obtener los datos del usuario
                setUserData(data); // Guarda los datos en el estado local
            } catch (error) {
                console.error("Error al obtener el perfil del usuario", error);
            } finally {
                setLoading(false); // Finaliza el estado de carga
            }
        };

        if (userId) {
            fetchUserProfile(); // Ejecuta la función al cargar el componente
        }
    }, [userId, actions]);

    // Petición para obtener los detalles de los productos favoritos
    useEffect(() => {
        const fetchFavoritesDetails = async () => {
            if (userData?.favorites?.length > 0) {
                try {
                    const details = await Promise.all(
                        userData.favorites.map((fav) => actions.getProductDetails(fav.product_id))
                    );
                    setFavoritesDetails(details); // Guardar los detalles en el estado
                } catch (error) {
                    console.error("Error al obtener los detalles de los favoritos", error);
                }
            }
        };

        if (userData) {
            fetchFavoritesDetails(); // Ejecuta la función si hay datos de usuario
        }
    }, [userData, actions]);

    if (loading) {
        return <p className="loging-data">Cargando datos del usuario...</p>;
    }

    if (!userData) {
        return <p className="loging-data">No se encontraron datos del usuario.</p>;
    }

    return (
        <div className="profile-container-log">
            <div className="profile-header-log row">
                <div className="profile-avatar-container-log col-xl-4 col-12">
                    <img
                        src={userData.avatar || "https://res.cloudinary.com/dshjlidcs/image/upload/v1738526759/j8e22hpsiepivnue4rby-min_dbfghd.png"}
                        alt="Avatar del usuario"
                        className="profile-avatar-log"
                    />
                </div>
                <div className="col-xl-8 col-12 mt-5">
                    <h1 className="profile-name-log">{userData.userName}</h1>
                    <p className="profile-email-log">{userData.email}</p>

                    <div className="profile-stats-log">
                        <span className="followers-log">{userData.followed_by.length} Seguidores</span>
                        <span className="following-log">{userData.following_users.length} Seguidos</span>
                    </div>
                </div>
            </div>
            <div className="profile-description-log">
                <p>{userData.description || "Descripción no proporcionada."}</p>
            </div>
            <h3 className="t-section">REVIEWS</h3>
            <div className="row pt-1 d-flex justify-content-center justify-content-lg-start">
                {store.reviews
                    ?.filter((review) => review.user_id === Number(userId))
                    .map((review) => (
                        <Reviews
                            key={review.id}
                            user_id={review.user_id}
                            rating={review.rating}
                            comment={review.comment}
                            product_id={review.product_id}
                        />
                    ))}
            </div>

            <h3 className="t-section">FAVORITOS</h3>
            <div className="horizontal-scrollable">
                <div className="row flex-nowrap pt-1">
                    {favoritesDetails.length > 0 ? (
                        favoritesDetails.map((fav) => (
                            <ProductCard
                                key={fav.id}
                                img={fav.img}
                                name={fav.name}
                                brand={fav.brand}
                                price={fav.price}
                                promoted={fav.promoted}
                                id={fav.id}
                            />
                        ))
                    ) : (
                        <p>No tienes productos favoritos.</p>
                    )}
                </div>
                <div className="divider"></div>
            </div>
        </div>
    );
};
