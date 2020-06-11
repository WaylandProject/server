import { KeyConstants } from 'utils/KeyConstants';

const controlsIds = {
    F11: 0x7A,
    W: 32,
    S: 33,
    A: 34,
    D: 35, 
    Space: 321,
    LCtrl: 326,
    LMB: 24,
	RMB: 25
};

var fly = {
    flying: false, f: 2.0, w: 2.0, h: 2.0, point_distance: 1000, l: 0
};
var gameplayCam = mp.cameras.new('gameplay');

let direction: any;
let coords: any;

function pointingAt(distance: any) {
    const farAway = new mp.Vector3((direction.x * distance) + (coords.x), (direction.y * distance) + (coords.y), (direction.z * distance) + (coords.z));

    const result = mp.raycasting.testPointToPoint(coords, farAway, undefined, 1 | 16);
    if (result === undefined) {
        return 'undefined';
    }
    return result;
}

// mp.events.add("AGM", (toggle) => {
// 	global.admingm = toggle;
// 	global.localplayer.setInvincible(toggle);
// 	mp.game.graphics.notify(toggle ? 'GM: ~g~Enabled' : 'GM: ~r~Disabled');
// });

mp.keys.bind(KeyConstants.Keys.VK_F10, false, function () {
    // check if player is admin
    const controls = mp.game.controls;
    const flyVar = fly;
    direction = gameplayCam.getDirection();
    coords = gameplayCam.getCoord();

    flyVar.flying = !flyVar.flying;

    const player = mp.players.local;

    // if(!global.admingm) player.setInvincible(fly.flying);
    player.freezePosition(flyVar.flying);
    player.setAlpha(flyVar.flying ? 0 : 255);

    if (!flyVar.flying && !controls.isControlPressed(0, controlsIds.Space)) {
        const position = mp.players.local.position;
        position.z = mp.game.gameplay.getGroundZFor3dCoord(position.x, position.y, position.z, 0.0, false);
        mp.players.local.setCoordsNoOffset(position.x, position.y, position.z, false, false, false);
    }

    mp.events.callRemote('invisible', flyVar.flying);
    mp.game.graphics.notify(flyVar.flying ? 'Fly: ~g~Enabled' : 'Fly: ~r~Disabled');
});

mp.events.add('render', () => {
    if (fly.flying) {
        const controls = mp.game.controls;
        const flyVar = fly;
        direction = gameplayCam.getDirection();
        coords = gameplayCam.getCoord();

        let updated = false;
        const position = mp.players.local.position;
		var speed;
        if(controls.isControlPressed(0, controlsIds.LMB)) speed = 1.0
		else if(controls.isControlPressed(0, controlsIds.RMB)) speed = 0.02
		else speed = 0.2
		if (controls.isControlPressed(0, controlsIds.W)) {
            if (flyVar.f < 8.0) flyVar.f *= 1.025;
            position.x += direction.x * flyVar.f * speed;
            position.y += direction.y * flyVar.f * speed;
            position.z += direction.z * flyVar.f * speed;
            updated = true;
        } else if (controls.isControlPressed(0, controlsIds.S)) {
            if (flyVar.f < 8.0) flyVar.f *= 1.025;
            position.x -= direction.x * flyVar.f * speed;
            position.y -= direction.y * flyVar.f * speed;
            position.z -= direction.z * flyVar.f * speed;
            updated = true;
        } else flyVar.f = 2.0;
        if (controls.isControlPressed(0, controlsIds.A)) {
            if (flyVar.l < 8.0) flyVar.l *= 1.025;
            position.x += (-direction.y) * flyVar.l * speed;
            position.y += direction.x * flyVar.l * speed;
            updated = true;
        } else if (controls.isControlPressed(0, controlsIds.D)) {
            if (flyVar.l < 8.0) flyVar.l *= 1.05;
            position.x -= (-direction.y) * flyVar.l * speed;
            position.y -= direction.x * flyVar.l * speed;
            updated = true;
        } else flyVar.l = 2.0;
        if (controls.isControlPressed(0, controlsIds.Space)) {
            if (flyVar.h < 8.0) flyVar.h *= 1.025;
            position.z += flyVar.h * speed;
            updated = true;
        } else if (controls.isControlPressed(0, controlsIds.LCtrl)) {
            if (flyVar.h < 8.0) flyVar.h *= 1.05;
            position.z -= flyVar.h * speed;
            updated = true;
        } else flyVar.h = 2.0;
        if (updated) mp.players.local.setCoordsNoOffset(position.x, position.y, position.z, false, false, false);
    }
});

mp.events.add('getCamCoords', (name) => {
    mp.events.callRemote('saveCamCoords', JSON.stringify(coords), JSON.stringify(pointingAt(fly.point_distance)), name);
});
