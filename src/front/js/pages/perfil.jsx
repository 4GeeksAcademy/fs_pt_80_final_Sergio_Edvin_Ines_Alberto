import React, { useContext, useState, useEffect } from "react";
import { Context } from "../store/appContext";
import "../../styles/perfil.css";
import { Link } from "react-router-dom";

import { FavCard } from "../component/fav-card.jsx";
import { Reviews } from "../component/reviews.jsx";

export const Perfil = () => {
    const { store, actions } = useContext(Context);
    const [userData, setUserData] = useState(null);
    const [showUserList, setShowUserList] = useState(false); // Estado para mostrar la lista de usuarios
    const [users, setUsers] = useState([]); // Estado para almacenar la lista de usuarios
    const [followedUsers, setFollowedUsers] = useState(new Set(userData?.following_users?.map(user => user.id) || []));
    const [favoritesDetails, setFavoritesDetails] = useState([]); // Detalles de productos favoritos

    useEffect(() => {
        const fetchUserData = async () => {
            const data = await actions.getUserProfile(store.user.id); // Obtiene el perfil del usuario actual
            setUserData(data);
            setFollowedUsers(new Set(data?.following_users.map(user => user.id))); // Guardamos los seguidos en local

            if (data?.favorites?.length > 0) {
                // Obtener los detalles de los productos favoritos
                const details = await Promise.all(
                    data.favorites.map(fav => actions.getProductDetails(fav.product_id))
                );
                setFavoritesDetails(details); // Guarda los detalles de los productos favoritos
            }
        };

        fetchUserData();
    }, [store.user.id]);

    // Función para obtener usuarios desde la API
    const fetchUsers = async () => {
        console.log("Cargando usuarios desde el action getAllUsers...");
        await actions.getAllUsers(); // Llama al action en flux.js
        const allUsers = store.users; // Lista global de usuarios desde el store

        // Actualizamos followedUsers para incluir la lista actualizada del usuario
        const updatedUserData = await actions.getUserProfile(store.user.id);
        setFollowedUsers(new Set(updatedUserData.following_users.map(user => user.id))); // Sincroniza los seguidos
        setUsers(allUsers); // Asigna la lista de usuarios al estado local
    };

    const handleFollowUser = async (userId) => {
        if (followedUsers.has(userId)) {
            // Si ya está seguido, lo dejamos de seguir
            await actions.unfollowUser(userId);
            setFollowedUsers(prev => {
                const updated = new Set(prev);
                updated.delete(userId);
                return updated;
            });
        } else {
            // Si no está seguido, lo seguimos
            await actions.followUser(userId);
            setFollowedUsers(prev => new Set(prev).add(userId));
        }

        // Refrescar el perfil del usuario actual después de seguir o dejar de seguir
        const updatedUserData = await actions.getUserProfile(store.user.id);
        setUserData(updatedUserData);
    };

    const handleLogout = () => {
        actions.logout(); // Llama a la función logout definida en flux.js
    };

    useEffect(() => {
        setUsers(store.users);
    }, [store.users]); // Se ejecuta cuando cambia la lista global de usuarios

    // Función para manejar el clic en el botón "+ Usuarios"
    const handleShowUserList = async () => {
        await fetchUsers();
        const offcanvasElement = document.getElementById("offcanvasUsers");
        let offcanvasInstance = bootstrap.Offcanvas.getInstance(offcanvasElement);

        if (!offcanvasInstance) {
            offcanvasInstance = new bootstrap.Offcanvas(offcanvasElement);
        }
        offcanvasInstance.show();
    };

    const [formData, setFormData] = useState({
        email: '',
        password: '',
        userName: ''
    });
    const [repeatPassword, setRepeatPassword] = useState('');

    const [formData1, setFormData1] = useState({
        email: "",
        password: ""
    });

    const [isRegister, setIsRegister] = useState(false);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({
            ...formData,
            [name]: value
        });
    };

    const [editData, setEditData] = useState({
        userName: userData?.userName || "",
        address: userData?.address || "",
        city: userData?.city || "",
        postalCode: userData?.postalCode || "",
        description: userData?.description || ""
    });

    const handleRepeatPasswordChange = (e) => {
        setRepeatPassword(e.target.value);
    };
    const handleChange1 = e => setFormData1({ ...formData1, [e.target.name]: e.target.value });

    const handleChange2 = (e) => {
        const { name, value } = e.target;
        setEditData(prevState => ({
            ...prevState,
            [name]: value
        }));
    };
    const handleSubmit = async (e) => {
        e.preventDefault();
        const updatedUser = await actions.updateUserProfile(store.user.id, editData);
    
        if (updatedUser) {
           
            setUserData(updatedUser);
            setIsEditing(false);  // Cierra el formulario de edición
        }
    };
    const [isEditing, setIsEditing] = useState(false); // Controla si el formulario de edición está visible

    useEffect(() => {
        window.scrollTo(0, 0);
    }, []);

    useEffect(() => {
        console.log("Estado de showUserList:", showUserList);
    }, [showUserList]);

    const filteredUsers = users.filter(user => user.id !== store.user.id);

    if (store.isLogged && !userData) {
        return <p className="loging-data">Cargando datos del usuario...</p>;
    }

    if (store.isLogged && userData) {
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
                        <div className="d-flex justify-content-between">
                            <div className="d-flex">
                                <h5 className="profile-name-log">{userData.userName}</h5>
                                <button className="btn btn-secondary float" onClick={handleLogout}>
                                    <span class="fa-solid fa-arrow-right-from-bracket ms-3"></span>
                                </button>
                            </div>
                            <button type="button" className="btn edit-btn float" onClick={() => setIsEditing(true)}>
                                <span className="fa-solid fa-pen-to-square"></span>
                            </button>

                        </div>
                        <p className="profile-email-log">{userData.email}</p>
                        <p className="profile-address-log">
                            {userData.address}, {userData.city} ({userData.postalCode})
                        </p>
                        <div className="profile-stats-log row justify-content-between">
                            <div className="col-md-6 col-12">
                                <span className="followers-log">{userData.followed_by.length} Seguidores</span>
                                <span className="following-log">{userData.following_users.length} Seguidos</span>
                            </div>

                            <span
                                className=" user-list-btn col-md-2 col-5 mt-2 ms-2"
                                onClick={handleShowUserList}
                            >
                                + Usuarios
                            </span>

                        </div>
                    </div>
                </div>
                {/* Modal de edición de perfil*/}
              {/* Formulario de edición, se muestra cuando isEditing es true */}
              {isEditing && (
                    <form onSubmit={handleSubmit} className="mt-4">
                        <div className="mb-3">
                            <label htmlFor="userName" className="form-label">Nombre de usuario</label>
                            <input
                                type="text"
                                className="my-form-control w-100"
                                id="userName"
                                name="userName"
                                value={editData.userName}
                                onChange={handleChange2}
                            />
                        </div>
                        <div className="mb-3">
                            <label htmlFor="address" className="form-label">Dirección</label>
                            <input
                                type="text"
                                className="my-form-control w-100"
                                id="address"
                                name="address"
                                value={editData.address}
                                onChange={handleChange2}
                            />
                        </div>
                        <div className="mb-3">
                            <label htmlFor="city" className="form-label">Ciudad</label>
                            <input
                                type="text"
                                className="my-form-control w-100"
                                id="city"
                                name="city"
                                value={editData.city}
                                onChange={handleChange2}
                            />
                        </div>
                        <div className="mb-3">
                            <label htmlFor="postalCode" className="form-label">Código Postal</label>
                            <input
                                type="text"
                                className="my-form-control w-100"
                                id="postalCode"
                                name="postalCode"
                                value={editData.postalCode}
                                onChange={handleChange2}
                            />
                        </div>
                        <div className="mb-3">
                            <label htmlFor="description" className="form-label">Descripción</label>
                            <textarea
                                className="my-form-control w-100"
                                id="description"
                                name="description"
                                value={editData.description}
                                onChange={handleChange2}
                            />
                        </div>
                        <button type="submit" className="btn btn-primary w-100">Guardar cambios</button>
                    </form>
                )}

                {/* Modal de lista de usuarios */}
                <div className="offcanvas offcanvas-end" tabIndex="-1" id="offcanvasUsers" aria-labelledby="offcanvasUsersLabel">

                    <div className="offcanvas-body users-offcanvas">
                        {users.length > 0 ? (
                            users.map(user => (
                                <div className="shopping-c-item p-2">
                                    <div key={user.id} className="user-item">
                                        <div className="d-flex">
                                            <img src={user.avatar} alt={user.userName} className="user-avatar" />
                                            <div >
                                                <div className="d-flex justify-content-between ">
                                                    <Link to={`/perfil/${user.id}`} className="user-name-link mt-2 ms-2">{user.userName}</Link>
                                                    <button className={`btn ${followedUsers.has(user.id) ? "btn-seguir" : "btn-seguido"}`}
                                                        onClick={() => handleFollowUser(user.id)}>
                                                        {followedUsers.has(user.id) ? <span class="fa-solid fa-user-minus"></span> : <span class="fa-solid fa-user-plus"></span>}
                                                    </button> </div>
                                                <p className="user-description ms-2">{user.description ? (user.description.length > 60 ? user.description.substring(0, 60) + "..." : user.description) : "Sin descripción"}</p>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            ))
                        ) : (
                            <p>No hay usuarios disponibles.</p>
                        )}
                    </div>
                </div>

                <div className="profile-description-log">
                    <p>{userData.description || "Nos encantaria saber algo mas de tí..."}</p>

                </div>
                {!userData.subscription && (
                    <Link to={`/suscripcion`} className="faq-home-button" style={{ maxWidth: "320px", textAlign: "center" }}>Hazte premium</Link>
                )}


                <h3 className="t-section">REVIEWS</h3>
                <div className="row pt-1 d-flex justify-content-center justify-content-lg-start">
                    {store.reviews
                        ?.filter((review) => review.user_id === Number(userData.id))
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
                <div className="profile-section-log">
                    <h3 className="t-section">FAVORITOS</h3>
                    <div className="horizontal-scrollable">
                        <div className="row flex-nowrap pt-1">
                            {favoritesDetails.length > 0 ? (
                                favoritesDetails.map((fav) => (
                                    <FavCard
                                        key={fav.id}
                                        img={fav.img}
                                        name={fav.name}
                                        brand={fav.brand}
                                        price={fav.price}
                                        promoted={fav.promoted}
                                        id={fav.id}
                                        removeFavorite={() => removeFav(fav.id)}
                                    />
                                ))
                            ) : (
                                <p>No tienes productos favoritos.</p>
                            )}
                        </div>
                    </div>
                    <div className="divider"></div>
                </div>

                {/* <div className="profile-section-log">
                    <h3 className="t-section">ESCAPARATE</h3>
                    <div className="showcase-container-log">
                        {userData.products?.length > 0 ? (
                            userData.products.map((product) => (
                                <div key={product.id} className="showcase-item-log">
                                    <img src={product.img} alt={product.name} className="showcase-img-log" />
                                    <p>{product.name}</p>
                                    <span>{product.price} €</span>
                                </div>
                            ))
                        ) : (
                            <p>No tienes productos en tu escaparate.</p>
                        )}
                    </div>
                </div> */}
            </div>
        );
    }

    return (
        <div className="container-fluid">
            <div className="row">
                {/* Sección de la imagen */}
                <div className="col-md-7 bg-image p-0 d-none d-md-block"></div>
                {/* Sección del formulario o botones iniciales */}
                <div className="col-md-5 d-flex align-items-center justify-content-center form-alt my-form-column" style={{ maxWidth: '550px' }}>
                    <div className="form-container rounded text-center">

                        {/* Si elige "Registrarse", muestra el formulario */}
                        {isRegister === true && (
                            <form
                                onSubmit={async (e) => {
                                    e.preventDefault(); // Prevenir la acción por defecto del formulario (recarga de página)

                                    const { email, password, userName } = formData;

                                    // Verificamos que las contraseñas coincidan
                                    if (password !== repeatPassword) {
                                        alert('Las contraseñas no coinciden');
                                        return;
                                    }

                                    // Crea un nuevo objeto solo con los campos necesarios para el backend
                                    const formDataForBackend = {
                                        email,
                                        password,
                                        userName
                                    };

                                    // Llamada a la acción de registro con los datos correctos
                                    await actions.register(formDataForBackend);
                                }}
                            >
                                <div className="text-center  mt-5 mb-lg-4">
                                    <h3>Crear Cuenta</h3>
                                </div>
                                <div className="mb-3">
                                    <label htmlFor="userName" className="form-label">
                                        Nombre de usuario*
                                    </label>
                                    <input
                                        type="text"
                                        className="my-form-control w-100"
                                        id="userName"
                                        placeholder="Nombre de usuario"
                                        required
                                        name="userName"
                                        value={formData.userName}
                                        onChange={handleChange}
                                    />
                                </div>
                                <div className="mb-3">
                                    <label htmlFor="email" className="form-label">
                                        Email*
                                    </label>
                                    <input
                                        type="email"
                                        className="my-form-control w-100"
                                        id="email"
                                        placeholder="ejemplo@ejemplo.com"
                                        required
                                        name="email"
                                        value={formData.email}
                                        onChange={handleChange}
                                    />
                                </div>
                                <div className="mb-3">
                                    <label htmlFor="password" className="form-label">
                                        Contraseña*
                                    </label>
                                    <input
                                        type="password"
                                        className="my-form-control w-100"
                                        id="password"
                                        placeholder="Contraseña"
                                        required
                                        name="password"
                                        value={formData.password}
                                        onChange={handleChange}
                                    />
                                </div>
                                <div className="mb-3">
                                    <label htmlFor="repeatPassword" className="form-label">
                                        Repetir Contraseña*
                                    </label>
                                    <input
                                        type="password"
                                        className="my-form-control w-100"
                                        id="repeatPassword"
                                        placeholder="Repite tu contraseña"
                                        required
                                        name="repeatPassword"
                                        value={repeatPassword} // Usamos el estado repeatPassword
                                        onChange={handleRepeatPasswordChange} // Manejamos su cambio con esta función
                                    />
                                </div>

                                <div className="d-flex flex-column">
                                    <button type="submit" className="btn faq-home-button mt-4">
                                        Crear perfil
                                    </button>

                                    <a
                                        className="btn-secondary mt-2"
                                        onClick={() => setIsRegister(false)}
                                    >
                                        Login
                                    </a>
                                </div>
                            </form>

                        )}

                        {/* Formulario de login */}
                        {isRegister === false && (
                            <form
                                onSubmit={async (e) => {
                                    e.preventDefault();
                                    actions.login(formData1);
                                }}
                            >
                                <div className="mb-3">
                                    <label htmlFor="email" className="form-label">Email*</label>
                                    <input
                                        type="email"
                                        className="my-form-control w-100"
                                        id="email"
                                        name="email"
                                        value={formData1.email}
                                        onChange={handleChange1}
                                        required
                                    />
                                </div>
                                <div className="mb-3">
                                    <label htmlFor="password" className="form-label">Contraseña*</label>
                                    <input
                                        type="password"
                                        className="my-form-control w-100"
                                        id="password"
                                        name="password"
                                        value={formData1.password}
                                        onChange={handleChange1}
                                        required
                                    />
                                </div>
                                <button type="submit" className="btn btn-primary w-100 mt-4">Iniciar sesión</button>
                                <button
                                    className="btn btn-primary w-100 mb-3 mt-4"
                                    onClick={() => setIsRegister(true)}
                                >
                                    Registrarse
                                </button>
                            </form>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};