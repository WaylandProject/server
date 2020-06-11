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

using System;
using GTANetworkAPI;
using Wayland.Utils;

namespace Wayland
{
    public class Main : Script
	{
		[ServerEvent(Event.ResourceStart)]
		public async void OnResourceStart()
		{
			Context.Init();
			var evnt = new PubSubEvent();
			evnt.EventName = PubSubEventsConstants.DefaultEvents.OnServerStart;
			await PubSub.Default.PublishAsync(evnt);
			NAPI.Util.ConsoleOutput("Wayland Project server started!");
		}

		[ServerEvent(Event.PlayerConnected)]
		public async void OnPlayerJoin(Player player) {
			var evnt = new PubSubEvent();
			evnt.EventName = PubSubEventsConstants.DefaultEvents.OnPlayerJoin;
			evnt.Payload.Add(EventPayloadConstants.Player, player);
			await PubSub.Default.PublishAsync(evnt);
		}

		[RemoteEvent("saveCamCoords")]
		public void SaveCameraCoords(Player player, string coords, string cameraPos, string name) {
			Console.WriteLine($"Coords: {coords}\nCamera pos: ${cameraPos}\nName: ${name}");
		}
	}
}
