function waitGame(status)
{
    if (status === true)
        document.getElementById("find_game_loader").style.display = "flex";
    else
        document.getElementById("find_game_loader").style.display = "none";
}

function waitTour(status)
{
    if (status === true)
        document.getElementById("find_tour_loader").style.display = "flex";
    else
        document.getElementById("find_tour_loader").style.display = "none";
}