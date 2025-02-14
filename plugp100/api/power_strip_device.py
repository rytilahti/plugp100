from plugp100.api.base_tapo_device import _BaseTapoDevice
from plugp100.api.tapo_client import TapoClient, Json
from plugp100.common.functional.either import Either
from plugp100.common.utils.json_utils import dataclass_encode_json
from plugp100.requests.set_device_info.set_plug_info_params import SetPlugInfoParams
from plugp100.requests.tapo_request import TapoRequest
from plugp100.responses.child_device_list import ChildDeviceList
from plugp100.responses.device_state import PlugDeviceState


class PowerStripDevice(_BaseTapoDevice):

    def __init__(self, api: TapoClient, address: str):
        super().__init__(api, address)

    async def get_state(self) -> Either[PlugDeviceState, Exception]:
        """
        The function `get_state` asynchronously retrieves device information and returns either the device state or an
        exception.
        @return: an instance of the `Either` class, which can hold either a `PlugDeviceState` object or an `Exception`
        object.
        """
        return (await self._api.get_device_info()) | PlugDeviceState.try_from_json

    async def get_children(self) -> Either[ChildDeviceList, Exception]:
        return await self._api.get_child_device_list()

    async def on(self, child_device_id: str) -> Either[True, Exception]:
        request = TapoRequest.set_device_info(dataclass_encode_json(SetPlugInfoParams(device_on=True)))
        return (await self._control_child(child_device_id, request)).map(lambda _: True)

    async def off(self, child_device_id: str) -> Either[True, Exception]:
        request = TapoRequest.set_device_info(dataclass_encode_json(SetPlugInfoParams(device_on=False)))
        return (await self._control_child(child_device_id, request)).map(lambda _: True)

    async def _control_child(self, device_id: str, request: TapoRequest) -> Either[Json, Exception]:
        return await self._api.control_child(device_id, request)
