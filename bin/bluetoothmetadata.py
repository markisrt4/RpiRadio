import dbus

# Define the dbus interface for metadata discovery
PLAYER_IFACE = "org.bluez.MediaPlayer1"

class BluetoothMetadata():
	def __init__(self):
		self.bus = dbus.SystemBus()
		self.player = None
		self.metadata = {}

		# Get the dbus object manager (for metadata)
		obj = self.bus.get_object("org.bluez", "/")
		self.manager = dbus.Interface(obj, "org.freedesktop.DBus.ObjectManager")

	def initialize(self):
		# Locate the managed objects 
		try:
			objects = self.manager.GetManagedObjects()
		except:
			objects = None

		if not objects:
			return False

		else:
			player_path = None
			# Loop through the objects in our manager ...
			for path, interfaces in objects.iteritems():

				# ... and see if we find a bluetooth player
				if PLAYER_IFACE in interfaces:
					player_path = path

			# We've found a player, so now we can get the metadata
			if player_path:
				print "player path=" + player_path
				self.player = self.bus.get_object("org.bluez", player_path)
				return True

			else:
				return False

	# Should be called periodically to update track information
	def tick(self):
		iface = "org.freedesktop.DBus.Properties"
		props = self.player.GetAll(PLAYER_IFACE, dbus_interface=iface)

		#for attr, value in props.items():
			#print(attr, '\t', value)

		# Check is there is a Track property (which contains track metadata)
		if props.get("Track", False):
			# Get the available metadata
			self.metadata["Title"]  = u"{}".format(props["Track"].get("Title"))
			self.metadata["Artist"] = u"{}".format(props["Track"].get("Artist"))
			self.metadata["Album"] = u"{}".format(props["Track"].get("Album"))
			self.metadata["Duration"] = u"{}".format(props["Track"].get("Duration"))
			self.metadata["Position"] = u"{}".format(props["Position"])

	def getTrackTitle(self):
		return self.metadata["Title"]

	def getTrackArtist(self):
		return self.metadata["Artist"]

	def getTrackAlbum(self):
		return self.metadata["Album"]

	def getTrackElapsedSeconds(self):
		return int(self.metadata["Position"]) / 1000
		
	def getTrackPercentageComplete(self):
		return (float(self.metadata["Position"]) / 1000 ) / (float(self.metadata["Duration"]) / 1000)
	
