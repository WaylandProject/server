/**
 * Copyright (C) 2020 ChronosX88
 * 
 * This file is part of Wayland Project Server.
 * 
 * Wayland Project Server is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 * 
 * Wayland Project Server is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with Wayland Project Server.  If not, see <http://www.gnu.org/licenses/>.
 */

import { RageEventConstants } from './utils/RageEventsConstants';
import { KeyConstants } from './utils/KeyConstants';
import { Utils } from './utils/Utils';

var authBrowser: BrowserMp

mp.events.add(RageEventConstants.Auth.ShowAuthScreen, () => {
    authBrowser = mp.browsers.new(Utils.generateUILink('login'));
    mp.gui.chat.show(false);
    mp.gui.cursor.show(true, true);
    let authCamera = mp.cameras.new('default', new mp.Vector3(788.1887817382812, 974.5294189453125, 380.5456237792969), new mp.Vector3(0,0,0), 40);
    authCamera.pointAtCoord(745.0472412109375, 1190.494873046875, 324.84991455078125);
    authCamera.setActive(true);
    mp.game.cam.renderScriptCams(true, false, 0, true, false);
})

mp.keys.bind(KeyConstants.Keys.VK_J, false, () => {
    authBrowser.destroy();
    mp.gui.chat.show(true);
    mp.gui.cursor.show(false, false);
    mp.game.cam.renderScriptCams(false, false, 0, true, false);
})