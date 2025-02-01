import React, { useContext, useState, useEffect } from "react";
import { Context } from "../store/appContext";
import "../../styles/perfil.css";
import { Link } from "react-router-dom";

export const Perfil = () => {
    const { store, actions } = useContext(Context);
    const [userData, setUserData] = useState(null);
    const [showUserList, setShowUserList] = useState(false); // Estado para mostrar la lista de usuarios
    const [users, setUsers] = useState([]); // Estado para almacenar la lista de usuarios
    const [followedUsers, setFollowedUsers] = useState(new Set(userData?.following_users.map(user => user.id) || []));
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
        console.log("Clic en + Usuarios");
        if (!showUserList) {
            await fetchUsers(); // Forzar la sincronización de usuarios y seguidores
        }
        setShowUserList(!showUserList);
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
    
    const handleRepeatPasswordChange = (e) => {
        setRepeatPassword(e.target.value);
    };
    const handleChange1 = e => setFormData1({ ...formData1, [e.target.name]: e.target.value });

    useEffect(() => {
        window.scrollTo(0, 0);
    }, []);

    useEffect(() => {
        console.log("Estado de showUserList:", showUserList);
    }, [showUserList]);

    const filteredUsers = users.filter(user => user.id !== store.user.id);

    if (store.isLogged && !userData) {
        return <p>Cargando datos del usuario...</p>;
    }

    if (store.isLogged && userData) {
        return (
            <div className="profile-container-log">
                <div className="profile-header-log">
                    <div className="profile-avatar-container-log">
                        <img
                            src={userData.avatar || "https://via.placeholder.com/150"}
                            alt="Avatar del usuario"
                            className="profile-avatar-log"
                        />
                        <div className="logout-button-container">
                            <button className="btn btn-secondary logout-btn" onClick={handleLogout}>
                                Cerrar sesión
                            </button>
                        </div>
                    </div>

                    <div className="profile-info-log">
                        <h1 className="profile-name-log">{userData.userName}</h1>
                        <p className="profile-email-log">{userData.email}</p>
                        <p className="profile-address-log">
                            {userData.address}, {userData.city} ({userData.postalCode})
                        </p>
                        <div className="profile-stats-log">
                            <span className="followers-log">{userData.followed_by.length} Seguidores</span>
                            <span className="following-log">{userData.following_users.length} Seguidos</span>
                            <button 
                                className="btn btn-primary user-list-btn" 
                                onClick={handleShowUserList}
                            >
                                + Usuarios
                            </button>
                        </div>
                    </div>
                </div>

                {/* Modal de lista de usuarios */}
                {showUserList && (
                    <div className="user-list-modal">
                        <h3 className="modal-title">Lista de Usuarios</h3>
                        <button className="close-modal" onClick={handleShowUserList}>X</button>
                        <div className="user-list">
                            {filteredUsers.length > 0 ? (
                                filteredUsers.map((user) => (
                                    <div key={user.id} className="user-item">
                                        <img src={user.avatar || "default-avatar.png"} alt={user.userName} className="user-avatar" />
                                        <div className="user-info">
                                            <Link to={`/perfil/${user.id}`} className="user-name-link">
                                                <h5>{user.userName}</h5>
                                            </Link>
                                            <p>{user.itemsForSale || 0} artículos en venta</p>
                                            <button 
                                                className={`btn btn-follow ${followedUsers.has(user.id) ? "followed" : ""}`} 
                                                onClick={() => handleFollowUser(user.id)}
                                            >
                                                {followedUsers.has(user.id) ? "Seguido" : "Seguir +"}
                                            </button>
                                        </div>
                                    </div>
                                ))
                            ) : (
                                <p>No hay usuarios disponibles.</p>
                            )}
                        </div>
                    </div>
                )}

                <div className="profile-description-log">
                    <p>{userData.description || "Descripción no proporcionada."}</p>
                    {!userData.subscription && (
                        <button className="btn-premium-log">Go Premium</button>
                    )}
                </div>
                <div className="profile-section-log">
                    <h2>Favoritos</h2>
                    <div className="horizontal-scrollable">
                        <div className="row flex-nowrap pt-1">
                            {favoritesDetails.length > 0 ? (
                                favoritesDetails.map((fav) => (
                                    <div key={fav.id} className="favorite-item-log">
                                        <img src={fav.img} alt={fav.name} className="favorite-img-log" />
                                        <p>{fav.name}</p>
                                        <span>{fav.price} €</span>
                                    </div>
                                ))
                            ) : (
                                <p>No tienes productos favoritos.</p>
                            )}
                        </div>
                    </div>
                </div>

                <div className="profile-section-log">
                    <h2>Escaparate</h2>
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
                </div>
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
                         <div className="text-center mb-4">
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