using System;
using GTANetworkAPI;

namespace Wayland
{
    public class Main : Script
	{
		[ServerEvent(Event.ResourceStart)]
		public void OnResourceStart()
		{
			NAPI.Util.ConsoleOutput("Example resource loaded!");
		}
	}
}
